from __future__ import absolute_import

import os.path
import numpy as np
from shapely.geometry import Polygon
from shapely.prepared import prep

from ocrd_modelfactory import page_from_file
from ocrd_models.ocrd_page import (
    MetadataItemType,
    LabelsType, LabelType,
    to_xml, CoordsType,
    TextLineType,
    TextRegionType,
    SeparatorRegionType,
    PageType
)
from ocrd_models.ocrd_page_generateds import (
    TableRegionType,
    ImageRegionType,
    RegionRefType,
    RegionRefIndexedType,
    OrderedGroupType,
    OrderedGroupIndexedType,
    UnorderedGroupType,
    UnorderedGroupIndexedType,
    ReadingOrderType
)
from ocrd import Processor
from ocrd_utils import (
    getLogger,
    concat_padded,
    coordinates_of_segment,
    coordinates_for_segment,
    points_from_polygon,
    polygon_from_points,
    MIMETYPE_PAGE
)

from .. import get_ocrd_tool
from .ocrolib import midrange
from .ocrolib import morph
from .common import (
    pil2array,
    array2pil,
    check_page, check_region,
    lines2regions
)

TOOL = 'ocrd-cis-ocropy-order'
LOG = getLogger('processor.OcropyOrder')

class OcropyOrder(Processor):

    def __init__(self, *args, **kwargs):
        self.ocrd_tool = get_ocrd_tool()
        kwargs['ocrd_tool'] = self.ocrd_tool['tools'][TOOL]
        kwargs['version'] = self.ocrd_tool['version']
        super(OcropyOrder, self).__init__(*args, **kwargs)

    def process(self):
        """Change the reading order of regions in pages or tables.
        
        Open and deserialise PAGE input files and their respective images,
        then iterate over the element hierarchy down to the requested level.
        
        Depending on ``level-of-operation``:
        - if ``page``, then consider the existing top-level text regions
          of the page, and delete the top-level ReadingOrder contents (if any),
        - if ``table``, then consider the existing top-level table regions
          of the page, and delete any (Un)OrderedGroup contents referring to them
        
        Next, get each segment image according to the layout annotation (from
        the alternative image of the page/table, or by cropping via coordinates
        into the higher-level image) in binarized form, and represent it as an array
        with non-text regions suppressed.
        
        Then compute a "segmentation" for that array (as a label mask).
        
        Text regions are detected via a hybrid variant of recursive X-Y cut
        algorithm: it partitions the binarized image in top-down manner by
        detecting horizontal or vertical gaps. This implementation uses the
        existing segmentation to guide the search, but also uses the existing
        separators to alternatively partition the respective boxes into
        non-rectangular parts.
        
        All regions are sorted according to their reading order (assuming a
        top-to-bottom, left-to-right ordering). When ``level-of-operation`` is
        ``page``, prefer vertical (column-first) succession of regions. When it is
        ``table``, prefer horizontal (row-first) succession of cells.
        
        Then create an OrderedGroup referencing all regions in the detected
        order.
        
        Produce a new output file by serialising the resulting hierarchy.
        """
        # FIXME: allow passing a-priori info on reading order / textline order
        # (and then pass on as ``bt`` and ``rl``; however, there may be a mixture
        #  of different scripts; also, vertical writing needs internal rotation
        #  because our line segmentation only works for horizontal writing)
        oplevel = self.parameter['level-of-operation']

        for (n, input_file) in enumerate(self.input_files):
            LOG.info("INPUT FILE %i / %s", n, input_file.pageId or input_file.ID)
            file_id = input_file.ID.replace(self.input_file_grp,
                                            self.output_file_grp)
            if file_id == input_file.ID:
                file_id = concat_padded(self.output_file_grp, n)

            pcgts = page_from_file(self.workspace.download_file(input_file))
            page_id = pcgts.pcGtsId or input_file.pageId or input_file.ID # (PageType has no id)
            page = pcgts.get_Page()
            
            # add metadata about this operation and its runtime parameters:
            metadata = pcgts.get_Metadata() # ensured by from_file()
            metadata.add_MetadataItem(
                MetadataItemType(type_="processingStep",
                                 name=self.ocrd_tool['steps'][0],
                                 value=TOOL,
                                 Labels=[LabelsType(
                                     externalModel="ocrd-tool",
                                     externalId="parameters",
                                     Label=[LabelType(type_=name,
                                                      value=self.parameter[name])
                                            for name in self.parameter.keys()])]))
            
            # TODO: also allow grayscale_normalized (try/except?)
            page_image, page_coords, page_image_info = self.workspace.image_from_page(
                page, page_id, feature_selector='binarized')
            if self.parameter['dpi'] > 0:
                zoom = 300.0/self.parameter['dpi']
            elif page_image_info.resolution != 1:
                dpi = page_image_info.resolution
                if page_image_info.resolutionUnit == 'cm':
                    dpi *= 2.54
                LOG.info('Page "%s" uses %f DPI', page_id, dpi)
                zoom = 300.0/dpi
            else:
                zoom = 1

            # aggregate existing regions so their foreground can be ignored
            seps = page.get_SeparatorRegion()
            # prepare reading order
            reading_order = dict()
            ro = page.get_ReadingOrder()
            if ro:
                rogroup = ro.get_OrderedGroup() or ro.get_UnorderedGroup()
                if rogroup:
                    page_get_reading_order(reading_order, rogroup)
            
            # get segments to process / overwrite
            if oplevel == 'page':
                ro = ReadingOrderType()
                page.set_ReadingOrder(ro)
                # new top-level group
                rogroup = OrderedGroupType(id="reading-order")
                ro.set_OrderedGroup(rogroup)
                self._process_element(page, seps, page_image, page_coords,
                                      page_id, file_id, zoom, rogroup=rogroup)
            elif oplevel == 'table':
                regions = list(page.get_TableRegion())
                if not regions:
                    LOG.warning('Page "%s" contains no table regions', page_id)
                for region in regions:
                    # TODO: also allow grayscale_normalized (try/except?)
                    region_image, region_coords = self.workspace.image_from_segment(
                        region, page_image, page_coords, feature_selector='binarized')
                    # create reading order group if necessary
                    roelem = reading_order.get(region.id)
                    if not roelem:
                        LOG.error("Page '%s' table region '%s' is not referenced in reading order (%s)",
                                  page_id, region.id, "no target to add cells to")
                        continue
                    else:
                        # replace regionRef(Indexed) by group with same index and ref
                        # (which can then take the cells as subregions)
                        roelem = page_subgroup_in_reading_order(roelem)
                        reading_order[region.id] = roelem
                    # go get TextRegions with TextLines (and SeparatorRegions)
                    self._process_element(region, seps, region_image, region_coords,
                                          region.id, file_id + '_' + region.id, zoom, roelem)
            
            # update METS (add the PAGE file):
            file_path = os.path.join(self.output_file_grp, file_id + '.xml')
            out = self.workspace.add_file(
                ID=file_id,
                file_grp=self.output_file_grp,
                pageId=input_file.pageId,
                local_filename=file_path,
                mimetype=MIMETYPE_PAGE,
                content=to_xml(pcgts))
            LOG.info('created file ID: %s, file_grp: %s, path: %s',
                     file_id, self.output_file_grp, out.local_filename)

    def _process_element(self, element, seps, image, coords, element_id, file_id, zoom, rogroup):
        """Add PAGE layout elements by segmenting an image.

        Given a PageType, TableRegionType or TextRegionType ``element``, and
        a corresponding binarized PIL.Image object ``image`` with coordinate
        metadata ``coords``, run line segmentation with Ocropy.
        
        If operating on the full page (or table), then also detect horizontal
        and vertical separators, and aggregate the lines into text regions
        afterwards.
        
        Add the resulting sub-segments to the parent ``element``.
        
        If ``ignore`` is not empty, then first suppress all foreground components
        in any of those segments' coordinates during segmentation, and if also
        in full page/table mode, then combine all separators among them with the
        newly detected separators to guide region segmentation.
        """
        regions = element.get_TextRegion()
        if not regions:
            LOG.warning('"%s" contains no text regions', element_id)
            return
        element_array = pil2array(image)
        element_bin = np.array(element_array <= midrange(element_array), np.bool)
        region_labels = np.zeros_like(element_bin, np.uint32)
        sep_bin = np.zeros_like(element_bin, np.bool)
        for i, sep in enumerate(seps):
            LOG.debug('masking foreground of separator "%s" for "%s"',
                      sep.id, element_id)
            sep_polygon = coordinates_of_segment(sep, image, coords)
            # If segment_polygon lies outside of element (causing
            # negative/above-max indices), either fully or partially,
            # then this will silently ignore them. The caller does
            # not need to concern herself with this.
            sep_bin[draw.polygon(sep_polygon[:, 1],
                                 sep_polygon[:, 0],
                                 sep_bin.shape)] = True
        for i, region in enumerate(regions):
            region_polygon = coordinates_of_segment(region, image, coords)
            region_labels[draw.polygon(region_polygon[:, 1],
                                       region_polygon[:, 0],
                                       region_labels.shape)] = i+1
        # suppress all fg outside of text regions
        element_bin = np.minimum(element_bin, region_labels)
        if isinstance(element, PageType):
            element_name = 'page'
            fullpage = True
            report = check_page(element_bin, zoom)
        elif isinstance(element, TableRegionType):
            element_name = 'table'
            fullpage = True
            report = check_region(element_bin, zoom)

        try:
            group_labels = lines2regions(
                element_bin, region_labels,
                sepmask=sep_bin,
                # decide horizontal vs vertical cut when gaps of similar size
                prefer_vertical=not isinstance(element, TableRegionType),
                gap_height=self.parameter['gap_height'],
                gap_width=self.parameter['gap_width'],
                zoom=zoom)
            LOG.info('Found %d text region clusters for %s "%s"',
                     len(np.unique(group_labels)) - 1,
                     element_name, element_id)
        except Exception as err:
            LOG.warning('Cannot region-segment %s "%s": %s',
                        element_name, element_id, err)
            group_labels = region_labels

        # prepare reading order group index
        if isinstance(rogroup, (OrderedGroupType, OrderedGroupIndexedType)):
            index = 0
            # start counting from largest existing index
            for elem in (rogroup.get_RegionRefIndexed() +
                         rogroup.get_OrderedGroupIndexed() +
                         rogroup.get_UnorderedGroupIndexed()):
                if elem.index >= index:
                    index = elem.index + 1
        else:
            index = None
        region_no = 0
        for group_label in np.unique(group_labels):
            if not group_label:
                continue # no bg
            # filter text regions within this group:
            group_region_labels = region_labels * (group_labels == group_label)
            for region_label in np.argsort(morph.reading_order(group_region_labels)):
                if not region_label:
                    continue
                index = page_add_to_reading_order(rogroup, regions[region_label-1].id, index)
                LOG.debug('Group label %d region label %d "%s"',
                          group_label, region_label, regions[region_label-1].id)


def polygon_for_parent(polygon, parent):
    """Clip polygon to parent polygon range.
    
    (Should be moved to ocrd_utils.coordinates_for_segment.)
    """
    childp = Polygon(polygon)
    if isinstance(parent, PageType):
        if parent.get_Border():
            parentp = Polygon(polygon_from_points(parent.get_Border().get_Coords().points))
        else:
            parentp = Polygon([[0,0], [0,parent.get_imageHeight()],
                               [parent.get_imageWidth(),parent.get_imageHeight()],
                               [parent.get_imageWidth(),0]])
    else:
        parentp = Polygon(polygon_from_points(parent.get_Coords().points))
    if childp.within(parentp):
        return polygon
    interp = childp.intersection(parentp)
    if interp.is_empty:
        # FIXME: we need a better strategy against this
        raise Exception("intersection of would-be segment with parent is empty")
    if interp.type == 'MultiPolygon':
        interp = interp.convex_hull
    return interp.exterior.coords[:-1] # keep open

def page_get_reading_order(ro, rogroup):
    """Add all elements from the given reading order group to the given dictionary.
    
    Given a dict ``ro`` from layout element IDs to ReadingOrder element objects,
    and an object ``rogroup`` with additional ReadingOrder element objects,
    add all references to the dict, traversing the group recursively.
    """
    if isinstance(rogroup, (OrderedGroupType, OrderedGroupIndexedType)):
        regionrefs = (rogroup.get_RegionRefIndexed() +
                      rogroup.get_OrderedGroupIndexed() +
                      rogroup.get_UnorderedGroupIndexed())
    if isinstance(rogroup, (UnorderedGroupType, UnorderedGroupIndexedType)):
        regionrefs = (rogroup.get_RegionRef() +
                      rogroup.get_OrderedGroup() +
                      rogroup.get_UnorderedGroup())
    for elem in regionrefs:
        ro[elem.get_regionRef()] = elem
        if not isinstance(elem, (RegionRefType, RegionRefIndexedType)):
            page_get_reading_order(ro, elem)

def page_add_to_reading_order(rogroup, region_id, index=None):
    """Add a region reference to an un/ordered RO group.
    
    Given a ReadingOrder group ``rogroup`` (of any type),
    append a reference to region ``region_id`` to it.
    
    If ``index`` is given, use that as position and return
    incremented by one. (This must be an integer if ``rogroup``
    is an OrderedGroup(Indexed).
    Otherwise return None.
    """
    if rogroup:
        if index is None:
            rogroup.add_RegionRef(RegionRefType(
                regionRef=region_id))
        else:
            rogroup.add_RegionRefIndexed(RegionRefIndexedType(
                regionRef=region_id, index=index))
            index += 1
    return index

def page_subgroup_in_reading_order(roelem):
    """Replace given RO element by an equivalent OrderedGroup.
    
    Given a ReadingOrder element ``roelem`` (of any type),
    first look up its parent group. Remove it from the respective
    member list (of its region refs or un/ordered groups),
    even if it already was an OrderedGroup(Indexed).
    
    Then instantiate an empty OrderedGroup(Indexed), referencing
    the same region as ``roelem`` (and using the same index, if any).
    Add that group to the parent instead.
    
    Return the new group object.
    """
    if not roelem:
        LOG.error('Cannot subgroup from empty ReadingOrder element')
        return roelem
    if not roelem.parent_object_:
        LOG.error('Cannot subgroup from orphan ReadingOrder element')
        return roelem
    if isinstance(roelem, (OrderedGroupType,OrderedGroupIndexedType)) and not (
            roelem.get_OrderedGroupIndexed() or
            roelem.get_UnorderedGroupIndexed() or
            roelem.get_RegionRefIndexed()):
        # is already a group and still empty
        return roelem
    if isinstance(roelem, (OrderedGroupType,
                           UnorderedGroupType,
                           RegionRefType)):
        getattr(roelem.parent_object_, {
            OrderedGroupType: 'get_OrderedGroup',
            UnorderedGroupType: 'get_UnorderedGroup',
            RegionRefType: 'get_RegionRef',
        }.get(roelem.__class__))().remove(roelem)
        roelem2 = OrderedGroupType(id=roelem.regionRef + '_group',
                                   regionRef=roelem.regionRef)
        roelem.parent_object_.add_OrderedGroup(roelem2)
        return roelem2
    if isinstance(roelem, (OrderedGroupIndexedType,
                           UnorderedGroupIndexedType,
                           RegionRefIndexedType)):
        getattr(roelem.parent_object_, {
            OrderedGroupIndexedType: 'get_OrderedIndexedGroup',
            UnorderedGroupIndexedType: 'get_UnorderedIndexedGroup',
            RegionRefIndexedType: 'get_RegionRefIndexed'
        }.get(roelem.__class__))().remove(roelem)
        roelem2 = OrderedGroupIndexedType(id=roelem.regionRef + '_group',
                                          index=roelem.index,
                                          regionRef=roelem.regionRef)
        roelem.parent_object_.add_OrderedGroupIndexed(roelem2)
        return roelem2
    return None
