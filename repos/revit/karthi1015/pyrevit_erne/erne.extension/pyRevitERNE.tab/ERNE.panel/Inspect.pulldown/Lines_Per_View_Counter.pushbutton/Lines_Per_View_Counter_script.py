"""
Lists lines per view in project
"""
# -*- coding: utf-8 -*-
import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import FilteredElementCollector as Fec
from Autodesk.Revit.DB import BuiltInCategory as Bic
from Autodesk.Revit.DB import ElementId
from collections import defaultdict
from rpw import doc
from rph.worksharing import get_elem_creator

view_lines = defaultdict(int)

lines_in_project = Fec(doc).OfCategory(Bic.OST_Lines).WhereElementIsNotElementType().ToElements()
lines = [l for l in lines_in_project]

for line in lines:
    if getattr(line, "OwnerViewId"):
        line_view_id = line.OwnerViewId.IntegerValue
        view_lines[line_view_id] += 1

for line_count, view_id in sorted(zip(view_lines.values(), view_lines.keys()), reverse=True):
    rvt_view_id = ElementId(view_id)
    view = doc.GetElement(rvt_view_id)
    if getattr(view, "Name"):
        view_name = doc.GetElement(rvt_view_id).Name
    else:
        view_name = "NoNameInDB"
    print('{} Lines in ViewId:{} ViewCreator: {} ViewName: {}'.format(
        str(line_count).rjust(6),
        str(view_id).rjust(9),
        get_elem_creator(None, elem_id=rvt_view_id).ljust(15),
        view_name.ljust(60)))

info = "{} lines in {} views ".format(len(lines), len(view_lines))
print(info)