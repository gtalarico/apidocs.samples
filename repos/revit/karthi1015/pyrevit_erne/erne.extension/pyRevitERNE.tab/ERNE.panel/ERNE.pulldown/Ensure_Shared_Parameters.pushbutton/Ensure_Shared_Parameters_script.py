"""
Ensures all shared parameters for pyRevit ERNE scripts are
available in current model - created if necessary
"""
from Autodesk.Revit.DB import BuiltInCategory as Bic
from Autodesk.Revit.DB import BuiltInParameterGroup as Bipg
from Autodesk.Revit.DB import ParameterType, Category
from Autodesk.Revit.DB import ExternalDefinitionCreationOptions
from System.Diagnostics import Stopwatch
from rpw import doc, db
import json
import os


def get_param_binding_info():
    pb_map = {
        "TypeBinding": {},
        "InstanceBinding": {},
    }
    pb_names = set()
    pb_iter = doc.ParameterBindings.ForwardIterator()
    pb_iter.Reset()
    while pb_iter.MoveNext():
        item = pb_iter.Current
        name = pb_iter.Key.Name
        binding = item.ToString().split(".")[-1]
        # print(name, item)
        pb_map[binding][name] = item
        pb_names.add(name)
    return pb_map, pb_names


def create_shared_parameters_from_spf_and_json(spf, json_spf_groups):
    param_bindings = doc.ParameterBindings
    for g in spf.Groups:
        print("")
        print(45 * "-")
        print(g.Name)
        for d in g.Definitions:
            print(35 * "-")
            print(d.Name, d.ParameterType.ToString())
            if d.Name not in pb_names:
                print("attempt to create param binding for: {}".format(d.Name))
                sp_info = json_spf_groups[g.Name][d.Name]
                rvt_group = sp_info["Group_parameter_under"]
                binding = BIND_METHODS[sp_info["Type_Instance"]]()
                print("binding is: {}".format(sp_info["Type_Instance"]))
                for cat_name in sp_info["Categories"]:
                    print("binding to category: {}".format(cat_name))
                    binding.Categories.Insert(get_category_from_bic(cat_name))
                param_bindings.Insert(d, binding, get_rvt_param_group(rvt_group))


def allow_text_params_vary_on_group():
    pb_iter = doc.ParameterBindings.ForwardIterator()
    pb_iter.Reset()
    while pb_iter.MoveNext():
        key = pb_iter.Key
        binding_type = pb_iter.Current.ToString().split(".")[-1]
        if binding_type == "TypeBinding":
            continue
        print(key.Name, key.ParameterType.ToString())
        if key.ParameterType.ToString() == "Text":
            key.SetAllowVaryBetweenGroups(doc, True)


def get_sp_dir():
    prefices = ["01", "18", "01_", "01_", "Re", "Ak"]
    search_dir = "J:"
    for prefix in prefices:
        for node in os.listdir(search_dir):
            if node.startswith(prefix):
                # print(node)
                search_dir = os.path.join(search_dir, node)
                # print search_dir
                break
    return search_dir


def get_category_from_bic(name):
    bic_attr = getattr(Bic, "OST_{}".format(name))
    return Category.GetCategory(doc, bic_attr)


def get_param_type(name):
    return getattr(ParameterType, name)


def get_rvt_param_group(name):
    return getattr(Bipg, "PG_{}".format(name.upper()))


stopwatch = Stopwatch()
stopwatch.Start()

BIND_METHODS = {
    "Type"    : doc.Application.Create.NewTypeBinding,
    "Instance": doc.Application.Create.NewInstanceBinding,
}

spf = doc.Application.OpenSharedParameterFile()
#print(spf.Filename)
SP_PATH_DEFINED = os.path.join(get_sp_dir(), "ERNE_shared_parameters.txt")

if not spf:
    doc.Application.SharedParametersFilename = SP_PATH_DEFINED
    print("set shared param file path to: {}".format(SP_PATH_DEFINED))
elif spf.Filename != SP_PATH_DEFINED:
    doc.Application.SharedParametersFilename = SP_PATH_DEFINED
    print("set shared param file path to: {}".format(SP_PATH_DEFINED))

spf = doc.Application.OpenSharedParameterFile()


# ensure pyRevit shared params from json are in shared param file

js_path = os.path.join(get_sp_dir(), "ERNE_pyRevit_required_shared_parameters.json")
with open(js_path) as js_file:
    json_spf_groups = json.load(js_file)


spf_group_names = {g.Name for g in spf.Groups}

for group_name in json_spf_groups:
    if not group_name in spf_group_names:
        print("did not find: {}".format(group_name))
        print("creating shared param group: {}".format(group_name))
        spf.Groups.Create(group_name)
    for name, info in json_spf_groups[group_name].items():
        print(name, info)
        spf_group = spf.Groups[group_name]
        existing_definitions = [d.Name for d in spf_group.Definitions]
        exists_already = name in existing_definitions
        if not exists_already:
            print("attempt to create: {}".format(name))
            def_opt = ExternalDefinitionCreationOptions(
                name,
                get_param_type(info["Type_of_parameter"]),
            )
            spf.Groups[group_name].Definitions.Create(def_opt)

for g in spf.Groups:
    print("")
    print(45*"-")
    print(g.Name)
    for d in g.Definitions:
        print(35*"-")
        print(d.Name, d.ParameterType.ToString().split(".")[-1])


# ensure pyRevit shared params are in current active model

pb_map, pb_names = get_param_binding_info()


for binding_type, binding_info in pb_map.items():
    print("")
    print(45*"-")
    print(binding_type)
    for name, binding in binding_info.items():
        print(35*"-")
        print(name)
        for cat in binding.Categories:
            print("  {}".format(cat.Name))


with db.Transaction("create needed parameters"):
    create_shared_parameters_from_spf_and_json(spf, json_spf_groups)


with db.Transaction("SP_SetAllowVaryBetweenGroups"):
    allow_text_params_vary_on_group()


print("\n{} ensure model shared params in: ".format(__file__))

stopwatch.Stop()
print(stopwatch.Elapsed)

