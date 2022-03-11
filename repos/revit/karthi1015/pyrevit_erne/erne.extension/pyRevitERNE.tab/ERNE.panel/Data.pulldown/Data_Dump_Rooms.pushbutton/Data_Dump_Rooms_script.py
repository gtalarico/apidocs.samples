"""
Collects rooms data into csv.
"""
import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import BuiltInCategory as Bic
from System.Diagnostics import Stopwatch
from rph import data_dump

stopwatch = Stopwatch()
stopwatch.Start()

count = data_dump.dump(
    typed_categories=[Bic.OST_Rooms],
)

for category, amount in count.items():
    print("{} instances of {} exported.".format(category, amount))
print("pyRevit dataDumpRooms run in: ")

stopwatch.Stop()
timespan = stopwatch.Elapsed
print(timespan)
