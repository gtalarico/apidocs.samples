import types
import sys
import re
import os
import pathlib
from pprint import pprint
from datetime import datetime
from prompt_toolkit import prompt
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from tinydb import TinyDB, Query
from utils.rms_paths import get_paths
from utils.bokeh_jobs_viz import update_graph
import subprocess
import colorful


# TODO adjust existing job
# TODO self-explaining collection of args and options


def exit_job_controller():
    """
    exits the job_controller
    """
    print("  exiting..")
    sys.exit()


def not_found(echo=None):
    """
    not implemented notification
    """
    if echo:
        if echo.startswith("#"):
            return
        elif echo.isdigit():
            show_db_job_by_id(int(echo))
            return
    print(f"  sorry this function is not implemented: {echo}")


def help():
    """
    lists implemented functions
    """
    for key, func in implemented.items():
        if key not in hidden:
            if func.__doc__:
                print(f"{key.rjust(32)}: {func.__doc__.strip()}")
            else:
                print(f"{key.rjust(15)}")


def list_db_jobs():
    """
    list all rms jobs from db
    """
    list_jobs()


def list_filtered_db_jobs():
    """
    list filtered rms jobs from db
    """
    print("  please enter project_code to filter by, return for all")
    prj_filter = prompt("> filter_db_jobs_by_project_number > ", **sub_prompt_options)
    print("  please enter command to filter by, return for all")
    cmd_filter = prompt("> filter_db_jobs_by_command > ", **sub_prompt_options)
    list_jobs(filter_prj=prj_filter, filter_cmd=cmd_filter)


def list_jobs(filter_prj=None, filter_cmd=None, by_id=None):
    db_results = []
    if by_id:
        job = rms_db.get(doc_id=by_id)
        if job:
            db_results.append(rms_db.get(doc_id=by_id))
        else:
            print(colorful.bold_red(f"  no job with id {by_id} found"))
    else:
        db_results = rms_db.all()
        if filter_cmd:
            db_results = rms_db.search(Query()["<command>"] == filter_cmd)
        if filter_prj:
            db_results = [r for r in db_results if filter_prj in r["<project_code>"]]
    if db_results:
        print(colorful.cyan("id".rjust(6)),
              colorful.cyan("project_code".ljust(18)),
              colorful.cyan("command".ljust(14)),
              colorful.cyan("start_time".rjust(12)),
              colorful.cyan("timeout".rjust(8)),
              )
        for job in db_results:
            job_id = job.doc_id
            job_timeout = job.get("timeout")
            if not job_timeout:
                job_timeout = 60
            print(str(job_id).rjust(6),
                  job["<project_code>"].ljust(18),
                  job["<command>"].ljust(14),
                  job[">start_time"].rjust(12),
                  str(job_timeout).rjust(8),
                  )
    else:
        print(colorful.bold_red("  no matching entries found."))


def add_job_to_db():
    """
    add job to database
    """
    print("  please enter required job arguments")
    args = collect_arguments(keys_to_collect=['<project_code>',
                                              '<command>',
                                              '<full_model_path>',
                                              '>start_time',
                                              ],
                             prompt_text='> enter job arguments >> ',)
    if args:
        print("  please enter job options, empty return to finish")
        options = collect_options(collector=[],
                                  prompt_text='> enter job options >> ')
        # print(options)
        db_job_dict = serdes(cmd_tokens={"args": args, "opts": options})
        pprint(db_job_dict)
        rms_db.upsert(db_job_dict, (Query()["<project_code>"] == args['<project_code>']) &
                                   (Query()["<command>"] == args['<command>']))


def remove_db_job_by_id(preset=None):
    """
    removes rms job from db by id
    """
    if preset:
        job_id = preset
    else:
        print("  please enter job_id to run")
        job_id = prompt("> run_job_by_db_id> ", **sub_prompt_options)
    job_id = int(job_id)
    job = rms_db.get(doc_id=job_id)
    if job:
        list_jobs(by_id=job_id)
        cmd_str = serdes(job=job)
        print(colorful.cyan("  got removed from db"))
        job = rms_db.remove(doc_ids=[job_id])
    else:
        print("  no job with this id found")


def run_db_job():
    """
    runs a job from database
    """
    print(" please enter: '<project_code>'")
    project_code = prompt("> run_job> ", **sub_prompt_options)
    print(" please enter: '<command>'")
    command = prompt("> run_job> ", **sub_prompt_options)
    print(f"to be run: 'python process_model.py {project_code} {command}'")
    job_id = rms_db.get((Query()["<project_code>"] == project_code) & (Query()["<command>"] == command)).doc_id
    job = rms_db.get(doc_id=job_id)
    if job_id:
        cmd_tokens = serdes(job=job[0])
        cmd_str = " ".join(cmd_tokens)
        if check_model_path(job_id):
            print(cmd_str)
            subprocess.Popen(cmd_str)
    else:
        print("  no job with this id found")


def run_db_job_by_id(preset=None):
    """
    runs a job from database by id
    """
    if preset:
        job_id = preset
    else:
        print("  please enter job_id to run")
        job_id = prompt("> run_job_by_db_id> ", **sub_prompt_options)
    if job_id:
        job_id = int(job_id)
        job = rms_db.get(doc_id=job_id)
        if job:
            # print(job)
            cmd_tokens = serdes(job=job)
            # print(cmd_tokens)
            cmd_str = " ".join(cmd_tokens)
            if check_model_path(job_id):
                print("cmd_str:", cmd_str)
                subprocess.Popen(cmd_str)
    else:
        print("  no job with this id found")


def check_model_path(job_id):
    job_id = int(job_id)
    job = rms_db.get(doc_id=job_id)
    model_path = pathlib.Path(job["<full_model_path>"])
    if model_path.exists():
        print(colorful.bold_green(f"  model found at: {model_path}"))
        return True
    else:
        print(colorful.bold_red(f"  could not find model at: {model_path}"))


def check_db_job_model_path_by_id(preset=None):
    """
    checks path of a model by job id
    """
    if preset:
        job_id = preset
    else:
        print("  please enter job_id to check for specific path, enter to check all paths")
        job_id = prompt("> check_model_path_exists_by_db_id> ", **sub_prompt_options)
    if job_id:
        check_model_path(job_id)
    else:
        for job in rms_db.all():
            job_id = job.doc_id
            check_model_path(job_id)


def show_db_job():
    """
    show config details of rms job from db
    """
    print("  please enter: '<project_code>'")
    project_code = prompt("> show_db_job> ", **sub_prompt_options)
    print("  please enter: '<command>'")
    command = prompt("> show_db_job> ", **sub_prompt_options)
    job = rms_db.search((Query()["<project_code>"] == project_code) & (Query()["<command>"] == command))
    if job:
        pprint(job[0])
    else:
        print("rms job not found")
    return


def show_db_job_by_id(preset=None):
    """
    show config details of rms job from db by id
    """
    if not preset:
        print("  please enter job_id to show details")
        job_id = prompt("> show_job_by_db_id> ", **sub_prompt_options)
        job_id = int(job_id)
    else:
        job_id = int(preset)
    job = rms_db.get(doc_id=job_id)
    if job:
        list_jobs(by_id=job_id)
        cmd_str = serdes(job=job)
        print(colorful.cyan("\n  command:"))
        print(cmd_str)
        return
    else:
        print("  no job with this id found")


def write_jobs_graph():
    """
    writes a html graph of jobs from db
    """
    update_graph(rms_db, rms_paths.db / "rms_jobs_timing.html")


def collect_options(collector=None, prompt_text='>> '):
    if not collector:
        collector = []
    # print(f"called collect_options with: {collector}")
    collected = prompt(prompt_text, **sub_prompt_options)
    # print(collector)
    if collected:
        collector.append(collected)
        # print(f"collected: {collected}")
        # print(f"collector: {collector}")
        collect_options(collector, prompt_text=prompt_text)
    # print(f"collector currently stores: {collector}")
    return collector


def collect_arguments(prompt_text='>> ', keys_to_collect=None):
    collector = {}
    if keys_to_collect:
        for key in keys_to_collect:
            collected = prompt(f"> {prompt_text} {key} >> ",
                               **sub_prompt_options)
            if collected:
                collector[key] = collected
            else:
                return
        return collector


def serdes(job=None, cmd_tokens=None):
    """
    serialize/deserialize job/commands hidden
    """
    if job:
        command = [f'"{sys.executable}"', f'"{rms_paths.root / "process_model.py"}"']
        command.extend([
            job["<command>"],
            job["<project_code>"],
            job["<full_model_path>"],
        ])
        for k, v in job.items():
            if k.startswith("<"):
                # print("arg: {} {}".format(k, v))
                pass
            elif k.startswith(">"):
                # print("event timer: {} {}".format(k, v))
                pass
            elif isinstance(v, bool):
                # command = " ".join([command, "--" + k])
                command.extend(["--" + k])
                # print("simple option: {} {}".format(k, v))
            else:
                # command = " ".join([command, " ".join(["--" + k, str(v)])])
                if "path" in k:
                    command.extend([" ".join(["--" + k, str(v).replace("'", '"')])])
                else:
                    command.extend([" ".join(["--" + k, str(v)])])
                # print("regular option: {} {}".format(k, str(v)))
        # print(command)
        return command
    if cmd_tokens:
        db_job_dict = {}
        # print(cmd_tokens)
        for arg in ['<command>', '<project_code>', '<full_model_path>', '>start_time']:
            db_job_dict[arg] = cmd_tokens["args"][arg]
        for opt in cmd_tokens["opts"]:
            opt_split = opt.split(" ")
            if len(opt_split) == 1:
                if opt.startswith("--"):
                    opt = opt[2:]
                db_job_dict[opt] = True
            elif len(opt_split) == 2:
                if opt_split[0].startswith("--"):
                    opt_split[0] = opt_split[0][2:]
                db_job_dict[opt_split[0]] = opt_split[1]
        return db_job_dict


def import_xmls_into_db():
    """
    import all xml rms tasks from db/xml_import directory into db
    """
    found_rms_task_xml = False
    for entry in os.scandir(rms_paths.xml_imp):
        if not entry.is_file():
            continue
        if not entry.name.endswith(".xml"):
            continue
        with open(rms_paths.xml_imp / entry.name, "r", encoding="utf-16le") as xml_task:
            xml_content = xml_task.read()
        re_process_model = re.compile("process_model.py")
        is_rms_task = re.findall(re_process_model, xml_content)
        if is_rms_task:
            print(colorful.bold_green(f"  processing xml: {entry.name}"))
            found_rms_task_xml = True
            cmd_tokens = {"args": {}, "opts": []}
            re_args = re.compile("Arguments>(.+)</Arguments")
            re_opts = re.compile("(--.+)",)
            re_start = re.compile("StartBoundary>.+T(.+)</StartBoundary")
            arguments = re.findall(re_args, xml_content)
            options = re.findall(re_opts, arguments[0])[0]
            cmd_args = arguments[0].split("--")[0].split()
            cmd_tokens["args"]["<command>"] = cmd_args[1]
            cmd_tokens["args"]['<project_code>'] = cmd_args[2]
            cmd_tokens["args"]["<full_model_path>"] = cmd_args[3]
            cmd_tokens["args"][">start_time"] = re.findall(re_start, xml_content)[0]
            cmd_tokens["opts"] = ["--" + tok.strip() for tok in options.split("--") if tok]
            # print(f"  found {cmd_tokens}")
            db_job_dict = serdes(cmd_tokens=cmd_tokens)  # {"args": args, "opts": options})
            pprint(db_job_dict)
            rms_db.upsert(db_job_dict, (Query()["<project_code>"] == cmd_tokens["args"]['<project_code>']) &
                          (Query()["<command>"] == cmd_tokens["args"]["<command>"]))
            print("  added/updated in db.")
    if not found_rms_task_xml:
        print(colorful.bold_red(f"  could not find rms task xml in: {rms_paths.db}"))


def export_xmls_from_db():
    """
    export all db jobs from db to db/xml_export directory
    """
    now_iso = datetime.now().isoformat()
    user = os.environ["USERNAME"]
    domain = os.environ["USERDOMAIN"]
    all_db_jobs = rms_db.all()

    print(now_iso, user, domain)

    for job in all_db_jobs:
        job_name = job["<project_code>"] + "_" + job["<command>"]
        start_time = now_iso.split("T")[0] + "T" + job[">start_time"]
        cmd_str = " ".join(serdes(job=job)[1:])
        # print(cmd_str)
        xml_prms = {r"\{user_id\}": f"{domain}\\\\{user}",
                    r"\{author\}": f"{domain}\\\\{user}",
                    r"\{description\}": f"created: {now_iso}",
                    r"\{creation_date\}": now_iso,
                    r"\{start_time\}": start_time,
                    r"\{application\}": sys.executable.replace("\\", "\\\\"),
                    r"\{args\}": cmd_str.replace("\\", "\\\\"),
                    }
        with open(rms_paths.xml_exp / "rms_xml_daily_template.xml", "r", encoding="utf-16le") as xml_template:
            xml_content = xml_template.read()

        for param in xml_prms:
            re_prm = re.compile(param)
            xml_content = re.sub(re_prm, xml_prms[param], xml_content)

        with open(rms_paths.xml_exp / f"{job_name}.xml", "w", encoding="utf-16le") as rms_export:
            rms_export.write(xml_content)

        print(colorful.bold_green(f"exported: {job_name}"))


def test_collected():
    # coll = collect_options()
    coll = collect_arguments(keys_to_collect=["a", "b", "c"])
    print(f" we got: {coll}")


rms_paths = get_paths(__file__)

FORMAT_JSON = {"sort_keys": True, "indent": 4, "separators": (',', ': ')}
rms_db = TinyDB(rms_paths.db / "jobs.json", **FORMAT_JSON)
history = InMemoryHistory()
suggest = AutoSuggestFromHistory()
hidden = [
    "prompt", "pprint", "not_found", "collect_options",
    "collect_arguments", "serdes", "list_jobs",
    "check_model_path", "test_collected", "style_from_dict",
    "get_paths", "update_graph"
]
implemented = {key: val for key, val in globals().items()
               if isinstance(val, types.FunctionType)
               and key not in hidden}
completer = WordCompleter([fn for fn in implemented.keys()])

prompt_options = dict(
    history=history,
    auto_suggest=suggest,
    completer=completer,
)

sub_prompt_options = dict(
    history=history,
    auto_suggest=suggest,
    completer=completer,
)

print("welcome to revit model services job controller.")
print("to list all functionality enter 'help'.")

while True:
    typed = prompt('> ', **prompt_options)
    if not typed:
        continue
    if typed.startswith("#"):
        continue
    if len(typed.split()) == 2:
        tokens = typed.split()
        func_name = tokens[0]
        arg = tokens[1]
        if implemented.get(func_name):
            perform = implemented.get(func_name)
            perform(preset=arg)
        continue
    else:
        if implemented.get(typed):
            perform = implemented.get(typed)
            perform()
            continue
    not_found(echo=typed)
