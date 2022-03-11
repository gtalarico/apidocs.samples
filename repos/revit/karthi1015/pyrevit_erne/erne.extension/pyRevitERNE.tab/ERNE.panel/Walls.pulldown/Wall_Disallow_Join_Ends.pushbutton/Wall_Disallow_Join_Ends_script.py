"""
Disallow join at both wall ends for selected walls.
"""

import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import WallUtils
from rpw import doc, uidoc, db
from System.Diagnostics import Stopwatch

stopwatch = Stopwatch()
stopwatch.Start()

selection = [doc.GetElement(elId) for elId in uidoc.Selection.GetElementIds()]

with db.Transaction("walls disallow join ends"):
    for elem in selection:
        if elem.Category.Name.ToString() == "Walls":
            WallUtils.DisallowWallJoinAtEnd(elem, 1)
            WallUtils.DisallowWallJoinAtEnd(elem, 0)

print("{} run in: ".format(__file__))
stopwatch.Stop()
timespan = stopwatch.Elapsed
print(timespan)
