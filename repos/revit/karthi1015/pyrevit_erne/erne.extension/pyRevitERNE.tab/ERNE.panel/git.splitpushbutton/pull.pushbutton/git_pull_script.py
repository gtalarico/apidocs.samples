from pyrevit import script
from pyrevit.loader.sessioninfo import get_session_uuid
from pyrevit.loader.sessionmgr import execute_command
from rph import git


def pyrevit_reload():
    PYREVIT_CORE_RELOAD_COMMAND_NAME = 'pyRevitCorepyRevitpyRevittoolsReload'
    execute_command(PYREVIT_CORE_RELOAD_COMMAND_NAME)
    script.get_results().newsession = get_session_uuid()


git.pull_repo("pyRevit_erne")
git.status_repo("pyRevit_erne")
pyrevit_reload()
