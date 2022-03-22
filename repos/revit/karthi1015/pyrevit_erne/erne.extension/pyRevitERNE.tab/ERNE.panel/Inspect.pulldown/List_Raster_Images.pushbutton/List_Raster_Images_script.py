"""
Lists raster images in project
"""
import clr
clr.AddReference("RevitAPI")
import Autodesk.Revit.UI
from Autodesk.Revit.DB import FilteredElementCollector as Fec
from Autodesk.Revit.DB import BuiltInCategory as Bic
from System.Diagnostics import Stopwatch
from collections import defaultdict
from pyrevit import script
from rpw import doc
from rph.worksharing import get_elem_creator


def report_img(img_type, img_insts_dict):
    img_id = output.linkify(img_type.Id)
    creator = get_elem_creator(img_type)
    type_name = img_type.LookupParameter("Type Name").AsString()
    insts_count = str(len(img_insts_dict[type_name]))
    inst_ids = ",".join([output.linkify(elem.Id) for elem in img_insts_dict[type_name]])
    # img_data = [img_id.ljust(10), creator.ljust(15), type_name, img_type.Path, insts_count, inst_ids]
    # this_script.output.print_md("<pre> Id:{} ; {} ; {} ; {} ; {} instances: ; {}</pre>".format(*img_data))
    img_type_data = [img_id.ljust(10), creator.ljust(15), type_name, img_type.Path]
    output.print_md("<pre> Id:{} ; {} ; {} ; {} </pre>".format(*img_type_data))
    output.print_md("<pre> {} instances: ; {}</pre>".format(insts_count.rjust(30), inst_ids))
    # print(inst_ids)


def count_raster_images(filter_paths=None):
    img_types = Fec(doc).OfClass(Autodesk.Revit.DB.ImageType).ToElements()
    img_insts = Fec(doc).OfCategory(Bic.OST_RasterImages).WhereElementIsNotElementType().ToElements()
    img_count = defaultdict(list)

    for img_inst in img_insts:
        img_type_name = doc.GetElement(img_inst.GetTypeId()).LookupParameter("Type Name").AsString()
        img_count[img_type_name].append(img_inst)

    if filter_paths:
        counter = 0
        for img in img_types:
            for path in filter_paths:
                if path in img.Path:
                    counter += 1
                    report_img(img, img_count)
        return counter

    else:
        for img in img_types:
            report_img(img, img_count)
        return img_types.Count


stopwatch = Stopwatch()
stopwatch.Start()

output = script.get_output()

non_project_paths = ["C:", "D:"]

print(40 * "-" + "all_raster_images")
count_all_images = count_raster_images()
print(40 * "-" + "non_project_raster_images")
count_non_project_images = count_raster_images(non_project_paths)

print("{} raster images types in non project paths found".format(count_non_project_images))

print("pyRevit findNonProjectPathImages run in: ")
stopwatch.Stop()
timespan = stopwatch.Elapsed
print(timespan)
