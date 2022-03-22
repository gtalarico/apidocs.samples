# -*- coding: utf-8 -*-
"""
Creates pyRevit scripts listing in AVAILABLE.md
Collects all required shared parameter data from scripts in json
"""
import os
import re
import json
from pprint import pprint


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


pyrvt_erne = r"C:\ProgramData\pyRevit_erne\erne.extension\pyRevitERNE.tab\ERNE.panel"
docs_md    = r"C:\ProgramData\pyRevit_erne\AVAILABLE.md"

# ::_Required_SP_:: T:YesNo; TI:Instance; G:Data; C:Doors, Rooms; SPG:GENERAL
re_param_info = re.compile(
    "# ::_Required_SP_:: "
    "T:(?P<Type_of_parameter>.+); "
    "TI:(?P<Type_Instance>.+); "
    "G:(?P<Group_parameter_under>.+); "
    "C:(?P<Categories>.+); "
    "SPG:(?P<Shared_Parameter_Group>.+)"
)

sp_data = []

script_count = 0

header = """
# List of available pyRevit erne scripts:
"""

with open(docs_md, "w") as md:
    md.write(header)
    for node in os.listdir(pyrvt_erne):
        if not os.path.isdir(os.path.join(pyrvt_erne, node)):
            continue
        dir_path = os.path.join(pyrvt_erne, node)
        script_cat = node.split(".")[0]
        print(35*"-")
        print(script_cat)
        md.write("\n## {}\n\n".format(script_cat))
        for subnode in os.listdir(dir_path):
            if not subnode.endswith("pushbutton"):
                continue
            #if not subnode.startswith("Create_Room_Floors"):
            #    continue
            sub_dir_path = os.path.join(dir_path, subnode)
            script_name = subnode.split(".")[0]
            script_py_file_name = script_name + "_script.py"
            script_py_path = os.path.join(sub_dir_path, script_py_file_name)
            if not os.path.exists(script_py_path):
                print("no .py found!!: {} !!!!".format(script_name))
                continue
            print(script_name)
            with open(script_py_path) as script:
                lines = script.readlines()
            doc_count = 0
            doc_string = ""
            for line in lines:
                if line.startswith('"""'):
                    doc_count += 1
                    continue
                if not doc_count == 1:
                    continue
                if doc_count == 2:
                    break
                doc_string += line
                #print(line)
            param_marker = "::_Required_SP_::"
            param_marker_line = ""
            param_lines = []
            for line in lines:
                if param_marker_line:
                    param_name = {" Name": line.split('"')[-2]}
                    print(param_name)
                    found = [m.groupdict() for m in re_param_info.finditer(param_marker_line)]
                    gd = found[0]
                    gd.update(param_name)
                    sp_data.append(gd)
                    param_doc = " <br>\n".join(["`{}: {}`".format(k, gd[k]) for k in sorted(gd)])
                    param_lines.append(param_doc + " <br>\n\n")
                    param_marker_line = ""
                if param_marker in line:
                    # print("found!!", line)
                    param_marker_line = line

            print(doc_string)
            # print(param_lines)
            print("")
            if doc_string:
                md.write("\n### {}\n\n".format(script_name))
                md.write(doc_string + "\n")
                if param_lines:
                    md.write("\n###### required parameters:\n\n")
                for param_string in param_lines:
                    md.write(param_string)

                script_count += 1


js_path = os.path.join(get_sp_dir(), "ERNE_pyRevit_required_shared_parameters.json")

sp_map = {}

for info in sp_data:
    # print(info)
    spg  = info.pop("Shared_Parameter_Group")
    name = info.pop(" Name")
    if spg not in sp_map:
        sp_map[spg] = {}
    if name not in sp_map[spg]:
        sp_map[spg][name] = {}

    for k, v in info.items():
        # print(k, v)
        if k == "Categories":
            v = [c.strip() for c in v.split(",")]
        sp_map[spg][name][k] = v

pprint(sp_map)

with open(js_path, "w") as js_file:
    json.dump(sp_map, js_file, indent=2)


print("found {} scripts with docstring".format(script_count))
print("written required sp info to: {}".format(js_path))

