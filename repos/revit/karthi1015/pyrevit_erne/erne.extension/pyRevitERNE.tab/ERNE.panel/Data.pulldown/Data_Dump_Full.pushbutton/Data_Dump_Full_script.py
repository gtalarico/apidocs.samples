"""
Collects floor data into csv.
"""
import clr
clr.AddReference("RevitAPI")
from System.Diagnostics import Stopwatch
from rph import data_dump

stopwatch = Stopwatch()
stopwatch.Start()

count = data_dump.dump()
for category, amount in count.items():
    print("{} instances of {} exported.".format(category, amount))
print("pyRevit dataDumpStrColumns run in: ")

stopwatch.Stop()
timespan = stopwatch.Elapsed
print(timespan)
