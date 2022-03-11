"""
Select Family Instances like doors and get
a listing of formula parameters.
"""
import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import FilteredElementCollector as Fec
from Autodesk.Revit.DB import BuiltInCategory as Bic
from collections import defaultdict
from System.Diagnostics import Stopwatch
from System import Enum
from pyrevit import script
from rpw import doc, uidoc


def get_family_insts_of_inst_bic(fam_instance):
    inst_cat = fam_instance.Category
    category_found = False
    for i, cat in enumerate(dir(Bic)):
        if str(cat).endswith(inst_cat.Name):
            category_found = True
    if not category_found:
        print("category not found")
        return
    for bic_cat in Enum.GetValues(Bic):
        if str(bic_cat).endswith("_" + inst_cat.Name):
            cat_insts = Fec(doc).OfCategory(bic_cat).WhereElementIsNotElementType().ToElements()
            return cat_insts


stopwatch = Stopwatch()
stopwatch.Start()
selection = [doc.GetElement(elId) for elId in uidoc.Selection.GetElementIds()]
output = script.get_output()

category_fams = set()
formula_params = defaultdict(dict)

if not selection:
    print("please select a family instance.")
else:
    category_insts = get_family_insts_of_inst_bic(selection[0])

    for fam_inst in category_insts:
        category_fams.add(fam_inst.Symbol.Family.Id)

    for fam_id in category_fams:
        fam = doc.GetElement(fam_id)
        fam_name = fam.Name
        fam_doc = doc.EditFamily(fam)
        fam_dims = Fec(fam_doc).OfCategory(Bic.OST_Dimensions).WhereElementIsNotElementType().ToElements()

        used_by_dim = set()
        for dim in fam_dims:
            if dim.NumberOfSegments < 2:
                if dim.FamilyLabel:
                    used_by_dim.add(dim.FamilyLabel.Definition.Name)
                    # print(dim.FamilyLabel.Definition.Name)

        print(55 * "-" + "\n" + fam_name)

        for param in fam_doc.FamilyManager.GetParameters():
            param_name = param.Definition.Name

            sp = "FP"
            if param.IsShared:
                sp = "SP"

            inst_param = "TP"
            if param.IsInstance:
                inst_param = "IP"

            dim_used = "no_Dim_"

            if param_name in used_by_dim:
                dim_used = "DimUsed"

            param_formula = param.Formula
            param_dtype = str(param.StorageType).split(".")[-1]

            if param_formula:
                formula_params[param_name][fam_name] = param_formula
                md_info = "<pre>{}-{}-{}-{}-{}-Formula: {}</pre>".format(
                    sp,
                    inst_param,
                    dim_used,
                    param_dtype.ljust(9),
                    param_name.ljust(30),
                    param_formula
                )
                output.print_md(md_info)

    print("\n" + 55 * "-" + "\n" + "Formula Overview" + "\n" + 55 * "-")

    for param_name in formula_params:
        used_by = len(formula_params[param_name])
        print("\n" + "Formula Parameter: {} used by {} Families:".format(param_name, used_by))
        print(35 * "-")
        for fam_name in formula_params[param_name]:
            output.print_md("<pre> {} @ {}</pre>".format(
                formula_params[param_name][fam_name],
                fam_name,
            ))

print("\n" + "run in: ")

stopwatch.Stop()
timespan = stopwatch.Elapsed
print(timespan)
