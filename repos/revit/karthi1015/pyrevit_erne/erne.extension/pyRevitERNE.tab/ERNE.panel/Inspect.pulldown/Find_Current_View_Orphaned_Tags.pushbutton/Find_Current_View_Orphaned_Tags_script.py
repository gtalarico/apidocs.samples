"""
Find orphaned tags showing ? in current view
"""
import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import FilteredElementCollector as Fec
from Autodesk.Revit.DB import IndependentTag, SpatialElementTag
from collections import defaultdict
from System.Diagnostics import Stopwatch
from rpw import doc
from rph.worksharing import get_elem_creator

stopwatch = Stopwatch()
stopwatch.Start()

rvt_version = doc.Application.VersionNumber
act_view = doc.ActiveView

i_tags = Fec(doc, act_view.Id).OfClass(IndependentTag).ToElements()
s_tags = Fec(doc, act_view.Id).OfClass(SpatialElementTag).ToElements()

orphaned_tag_views = defaultdict(list)
orphaned_tag_counter = 0

for i_tag in i_tags:
    if i_tag.IsOrphaned:
        tag_view_id = i_tag.OwnerViewId
        orphaned_tag_views[tag_view_id].append(i_tag)

# only working from rvt 2017 onwards
if int(rvt_version) > 2016:
    for s_tag in s_tags:
        if s_tag.IsOrphaned:
            tag_view_id = s_tag.OwnerViewId
            orphaned_tag_views[tag_view_id].append(s_tag)

for view_id in orphaned_tag_views:
    tag_view_name = doc.GetElement(view_id).Name
    print(50 * "_" + tag_view_name)
    for tag in orphaned_tag_views[view_id]:
        orphaned_tag_counter += 1
        tag_creator = get_elem_creator(tag)
        print(" Id: {} {} {}".format(tag.Id.IntegerValue, tag_creator, tag.Category.Name))

print("pyRevit findOrphanedTags found {} orphaned tags run in:".format(orphaned_tag_counter))
stopwatch.Stop()
timespan = stopwatch.Elapsed
print(timespan)
