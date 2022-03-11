"""
Find orphaned tags showing ? in project
"""
# -*- coding: utf-8 -*-
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
rvt_version_warning = False

act_view = doc.ActiveView

i_tags = Fec(doc).OfClass(IndependentTag).ToElements()
s_tags = Fec(doc).OfClass(SpatialElementTag).ToElements()

view_names = defaultdict(object)
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
else:
    rvt_version_warning = True

for view_id in orphaned_tag_views:
    view_name = doc.GetElement(view_id).Name
    view_names[view_name] = view_id

for view_name in sorted(view_names):
    print(50 * "_" + view_name)
    for tag in orphaned_tag_views[view_names[view_name]]:
        orphaned_tag_counter += 1
        tag_creator = get_elem_creator(tag)
        print(" Id: {} {} {}".format(tag.Id.IntegerValue, tag_creator, tag.Category.Name))

print("pyRevit findOrphanedTags found " + str(orphaned_tag_counter) + " orphaned tags run in: ")
stopwatch.Stop()
timespan = stopwatch.Elapsed
print(timespan)
