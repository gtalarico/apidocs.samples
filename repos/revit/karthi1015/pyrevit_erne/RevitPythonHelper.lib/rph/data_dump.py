# -*- coding: cp1252 -*-
import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import FilteredElementCollector as Fec
from Autodesk.Revit.DB import BuiltInCategory as Bic
from Autodesk.Revit.DB import ElementId
import os
import re
from datetime import datetime
from collections import defaultdict, OrderedDict
from pyrevit import script
from rpw.ui.forms import select_folder
from rpw import doc


def compile_category_params(elements):
    param_names = set()

    for element in elements:
        for param in element.Parameters:
            param_name = param.Definition.Name
            param_names.add(param_name)

    return sorted(list(param_names))


def collect_param_values(element, parameter_names):
    param_values = OrderedDict()

    for param_name in parameter_names:
        param_value = ""
        param = element.LookupParameter(param_name)

        if param:
            if param.HasValue:
                storage_type = param.StorageType.ToString()
                if storage_type == "ElementId":
                    param_value = param.AsElementId().IntegerValue.ToString()
                    if param_name in elem_id_clear_value_params:
                        elem_id = param.AsElementId()
                        if not elem_id == ElementId.InvalidElementId:
                            param_value = doc.GetElement(param.AsElementId()).Name
                elif storage_type == "Integer":
                    param_value = param.AsValueString()
                elif storage_type == "Double":
                    param_value = param.AsValueString()
                elif storage_type == "String":
                    param_value = param.AsString()
        param_value = param_value or ""
        param_values[param_name] = param_value.replace("\r\n", "").replace("\n", "").replace("\r", "")

    return param_values


def get_export_path():
    if os.environ.get("RVT_DATA_DUMP_PATH"):
        return os.environ["RVT_DATA_DUMP_PATH"]
    else:
        return select_folder()


def get_elem_location(element):
    if "GetTotalTransform" in dir(element):
        return element.GetTotalTransform().Origin.ToString()
    else:
        return ""


def dump(typed_categories=None, untyped_categories=None, export_path=None, filters=None):
    """
    Writes element data for chosen categories, ids, location and params to specified csv
    with the possibility to filter: e.g. {'type':{'Type Name':r"^[X][X]_.+"}}
    :param optional list of typed_categories: e.g. [BIC_Doors]
    :param optional list of untyped_categories: e.g. [BIC_Rooms]
    :param export_path: as path string e.g. "c:/temp/rvt_data_dump"
    :param filters: dict of {'inst/type': {'param_name': 'regex_str_for_param_for_elems_to_keep'}}
    :return:
    """
    output = script.get_output()
    today = datetime.now().strftime("%Y%m%d")
    today_time = datetime.now().strftime("%Y%m%d_%H%M")

    if not typed_categories and not untyped_categories:
        typed_categories   = typical_typed_categories
        untyped_categories = typical_untyped_categories

    categories = {
        "typed"  : typed_categories   or [],
        "untyped": untyped_categories or [],
    }

    model_name = os.path.basename(doc.PathName)
    if not export_path:
        export_path = get_export_path()
        if not export_path:
            print("please provide a working export dir. aborting.")
            return
    os.path.join(export_path, "{}_data_dump_{}".format(today, model_name))
    print("exporting to: {}".format(export_path))
    if not os.path.exists(export_path):
        os.makedirs(export_path)

    exported_instances        = defaultdict(int)
    category_param_names      = defaultdict(list)
    category_type_param_names = defaultdict(list)
    progress = 0
    progress_total = len(categories["typed"]) + len(categories["untyped"])

    for typing in categories:
        print(40 * "-" + typing)
        for bic in categories[typing]:
            progress += 1
            output.update_progress(progress, progress_total)
            cat_name = bic.ToString().split("_")[-1]
            print("__current category: {}".format(cat_name))

            instances = Fec(doc).OfCategory(bic).WhereElementIsNotElementType().ToElements()
            if not instances:
                continue

            category_param_names[cat_name] = compile_category_params(instances)

            if typing == "typed":
                types = Fec(doc).OfCategory(bic).WhereElementIsElementType().ToElements()
                category_type_param_names[cat_name] = compile_category_params(types)

            csv_name = "{}_{}.csv".format(today_time, cat_name)
            csv_path = os.path.join(export_path, csv_name)
            with open(csv_path, "w") as cat_csv:
                print("  writing: {}".format(csv_path))

                header = ";".join([name for name in category_param_names[cat_name]])
                type_header = ""
                if typing == "typed":
                    type_header = ";" + ";".join([name for name in category_type_param_names[cat_name]])

                cat_csv.write("rvt_id;GUID;location;" + header + type_header + "\n")

                for inst in instances:
                    inst_params_vals = collect_param_values(inst, category_param_names[cat_name])
                    inst_type = doc.GetElement(inst.GetTypeId())
                    location = get_elem_location(inst)
                    ids_loc = "{};{};{};".format(inst.Id.ToString(), inst.UniqueId, location)

                    info_line = ids_loc + ";".join([val for val in inst_params_vals.values()])

                    if typing == "typed":
                        type_params_vals = collect_param_values(inst_type, category_type_param_names[cat_name])
                        info_line += ";" + ";".join([val for val in type_params_vals.values()])

                    match = True
                    if filters:
                        match = False
                        if filters.get('type'):
                            for type_param_name_filter in  filters['type']:
                                re_param = re.compile(filters['type'][type_param_name_filter])
                                param_val = type_params_vals[type_param_name_filter]
                                if re.match(re_param, param_val):
                                    match = True
                                    break
                        elif filters.get('inst'):
                            for inst_param_name_filter in  filters['inst']:
                                re_param = re.compile(filters['inst'][inst_param_name_filter])
                                param_val = inst_params_vals[type_param_name_filter]
                                if re.match(re_param, param_val):
                                    match = True
                                    break
                    if match:
                        cat_csv.write(info_line + "\n")
                        exported_instances[cat_name] += 1

                print(40 * "-")
    return exported_instances


elem_id_clear_value_params = {
    "Level",
    "Top Constraint",
    "Base Constraint",
    "Base Level",
}

typical_typed_categories = [
    Bic.OST_Casework,
    Bic.OST_Ceilings,
    Bic.OST_CurtainWallMullions,
    Bic.OST_CurtainWallPanels,
    Bic.OST_Doors,
    Bic.OST_ElectricalEquipment,
    Bic.OST_ElectricalFixtures,
    Bic.OST_Floors,
    Bic.OST_Furniture,
    Bic.OST_GenericModel,
    Bic.OST_Grids,
    Bic.OST_Levels,
    Bic.OST_LightingFixtures,
    Bic.OST_PlumbingFixtures,
    Bic.OST_Ramps,
    Bic.OST_RoofSoffit,
    Bic.OST_Roofs,
    Bic.OST_Site,
    Bic.OST_SpecialityEquipment,
    Bic.OST_StackedWalls,
    Bic.OST_Stairs,
    Bic.OST_StairsLandings,
    Bic.OST_StairsRuns,
    Bic.OST_StructuralColumns,
    Bic.OST_StructuralFraming,
    Bic.OST_Walls,
]

typical_untyped_categories = [
    Bic.OST_Areas,
    Bic.OST_Rooms,
]
