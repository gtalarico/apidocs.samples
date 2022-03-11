import os
import clr
clr.AddReference("System")
import System
clr.AddReference("LibGit2Sharp")
from LibGit2Sharp import Repository, Commands
from LibGit2Sharp import FetchOptions, PullOptions, StatusOptions
from LibGit2Sharp import Signature, Identity


def pull_repo(name):
    print("INFO: git pull: {}".format(name))
    target_path = os.path.join(PROG_DATA, name)
    repo = Repository(str(target_path))
    pull_opt = PullOptions()
    now = System.DateTimeOffset.Now
    sig =  Signature(Identity("merger", "merger"), now)
    merge_result = Commands.Pull(repo, sig, pull_opt)
    print(merge_result.Status)


def status_repo(name):
    print("INFO: git status: {}".format(name))
    target_path = os.path.join(PROG_DATA, name)
    repo = Repository(str(target_path))
    status = repo.RetrieveStatus(StatusOptions())
    if status.IsDirty:
        print("repo not clean - please contact your pyRevit admin!")
        return
    print("repo is clean: {}".format(not status.IsDirty))


PROG_DATA = "C:\\ProgramData"
