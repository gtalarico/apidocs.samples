"""
Lists elements joined to selected element
"""
import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import FilteredElementCollector as Fec
from Autodesk.Revit.DB import JoinGeometryUtils
from System.Diagnostics import Stopwatch
from rpw import doc, uidoc
from pyrevit import script, forms


def correct_selection():
    if len(selection) == 1:
        return True


stopwatch = Stopwatch()
stopwatch.Start()

output = script.get_output()
selection = [doc.GetElement(elId) for elId in uidoc.Selection.GetElementIds()]
all_elements = Fec(doc).WhereElementIsNotElementType().ToElements()

if not correct_selection():
    forms.alert('Exactly one element must be selected.', exitscript=True)

joined_elem = selection[0]
print("Your selected element is joined with:")
for elem in all_elements:
    if JoinGeometryUtils.AreElementsJoined(doc, elem, joined_elem):
        print("{} - Id: {}".format(
            elem.Category.Name,
            output.linkify(elem.Id),
        ))


print("\n{}run in: ".format(__file__))
stopwatch.Stop()
timespan = stopwatch.Elapsed
print(timespan)
