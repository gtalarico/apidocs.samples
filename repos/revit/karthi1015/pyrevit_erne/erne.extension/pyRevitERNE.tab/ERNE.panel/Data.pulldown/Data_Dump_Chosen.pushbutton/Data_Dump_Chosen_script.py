"""
Collects data of selected category elements into csv.
"""
import clr
clr.AddReference("RevitAPI")
from System.Diagnostics import Stopwatch
from rph import data_dump
from rpw.ui.forms import FlexForm, CheckBox, Button

category_list = data_dump.typical_typed_categories
category_list.extend(data_dump.typical_untyped_categories)

category_map = {str(cat): cat for cat in category_list}

components = [CheckBox(str(cat), str(cat)[3:]) for cat in sorted(category_map)]
components.append(Button('Select'))
form = FlexForm('Choose categories for data dump', components)
form.show()

chosen_categories = []
print("chosen categories:")
for name, value in form.values.items():
    if value:
        print(name)
        chosen_categories.append(category_map[name])

stopwatch = Stopwatch()
stopwatch.Start()

count = data_dump.dump(
    chosen_categories
)
for category, amount in count.items():
    print("{} instances of {} exported.".format(amount, category))
print("pyRevit dataDumpChosen run in: ")

stopwatch.Stop()
timespan = stopwatch.Elapsed
print(timespan)
