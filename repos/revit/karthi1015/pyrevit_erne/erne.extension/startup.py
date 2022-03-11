import sys
import os

pyRevit_erne_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(pyRevit_erne_root, "RevitPythonHelper.lib"))

print("welcome to pyRevit_erne!\nrunning auto updater..\n")

from rph import git
git.pull_repo("pyRevit_erne")
git.status_repo("pyRevit_erne")

