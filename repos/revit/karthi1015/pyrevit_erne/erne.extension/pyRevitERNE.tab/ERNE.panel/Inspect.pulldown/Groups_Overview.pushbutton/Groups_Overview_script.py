"""
Lists groups in project
"""
import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import FilteredElementCollector as Fec
from Autodesk.Revit.DB import BuiltInCategory as Bic
from Autodesk.Revit.DB import GroupType
from System.Diagnostics import Stopwatch
from collections import defaultdict
from pyrevit import script
from rpw import doc
from rph.worksharing import get_elem_creator


def report_groups(collector, group_dict):
    counts = []
    for group in collector:
        if not group_dict[group.Name]:
            group_dict[group.Name] = {"last_id": "", "count": 0}
        group_dict[group.Name]["last_id"] = group.Id
        group_dict[group.Name]["count"] += 1

    for group in group_dict:
        counts.append(group_dict[group]["count"])

    for count, name in sorted(zip(counts, group_dict), reverse=True):
        click_id = output.linkify(group_dict[name]["last_id"])
        creator = get_elem_creator(None, elem_id=group_dict[name]["last_id"])
        md_info = "<pre>{} last Id: {} by: {} has {} Instances</pre>".format(
            name.ljust(50),
            click_id,
            creator.ljust(12),
            count,
        )
        output.print_md(md_info)


stopwatch = Stopwatch()
stopwatch.Start()

output = script.get_output()

groups_types       = Fec(doc).OfClass(GroupType).ToElements()
model_group_insts  = Fec(doc).OfCategory(Bic.OST_IOSModelGroups ).WhereElementIsNotElementType().ToElements()
detail_group_insts = Fec(doc).OfCategory(Bic.OST_IOSDetailGroups).WhereElementIsNotElementType().ToElements()

model_groups  = defaultdict(list)
detail_groups = defaultdict(list)

print("group_types           : {}".format(len((groups_types))))
print("model_group_instances : {}".format(len((model_group_insts))))
print("detail_group_instances: {}".format(len((detail_group_insts))))

print(68 * "-" + "Model_Groups")
report_groups(model_group_insts, model_groups)
print(68 * "-" + "Detail_Groups")
report_groups(detail_group_insts, detail_groups)

print("pyRevit_groups_overview listed in: ")
stopwatch.Stop()
timespan = stopwatch.Elapsed
print(timespan)
