"""
Lists materials in project
"""
import clr
clr.AddReference("RevitAPI")
import Autodesk.Revit.UI
from Autodesk.Revit.DB import FilteredElementCollector as Fec
from collections import defaultdict
from System.Diagnostics import Stopwatch
from rpw import doc
from rph.worksharing import get_elem_creator

stopwatch = Stopwatch()
stopwatch.Start()

mats = Fec(doc).OfClass(Autodesk.Revit.DB.Material          ).ToElements()
pats = Fec(doc).OfClass(Autodesk.Revit.DB.FillPatternElement).ToElements()

mats_dict = defaultdict(list)

for i, mat in enumerate(mats):
    mat_cut_pattern_name = getattr(mat, "Name") or ""
    if mat_cut_pattern_name:
        mats_dict[mat.Id].append([mat.Name, mat_cut_pattern_name])

    print('{} Id: {} Material: {} MaterialCreator: {} CutPattern: {}'.format(
        str(i).zfill(3).rjust(4),
        str(mat.Id.IntegerValue).rjust(8),
        str(mat.Name.decode("utf-8", "replace")).ljust(45),
        get_elem_creator(mat).ljust(11),
        str(mat_cut_pattern_name.decode("utf-8", "replace")).ljust(70)))


print("pyRevit materials overview run in: ")
stopwatch.Stop()
timespan = stopwatch.Elapsed
print(timespan)
