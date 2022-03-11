"""
Update Code Samples

Usage:
    python update.py

refact for windows setup jmcouffin [at] gmail [dot] com
"""

import os
import json
import subprocess
import pathlib

# Current directory
cwd = pathlib.PureWindowsPath(os.getcwd()).as_posix()
# Current directory for repos
cwd_repos = pathlib.PureWindowsPath(os.getcwd()).as_posix() + "\\repos"
# Extensions (kept)
extensions = ('.py', '.cs')
# Get repos.json data
with open('repos.json') as fp:
    repos = json.load(fp)

# remove the repos folder before cloning the git
if os.path.exists(cwd_repos):
    repos_folder = cwd_repos.replace('/', '\\')
    print("Repos folder exists: " + repos_folder)
    cmd = f"""rmdir /q /s  {repos_folder}"""
    output = subprocess.check_output(cmd, shell=True)

# cloning the repos
for repo_info in repos:
    repo_path = repo_info['path']
    git_url = repo_info['url']
    cmd = f"""git clone --depth=1 "{git_url}" {repo_path}"""
    output = subprocess.check_output(cmd, shell=True)

# remove git folder
for repo_info in repos:
    # not the most elegant way to handle fpath, but it works (windows)
    repo_path = cwd + '\\' + \
        str(pathlib.PureWindowsPath(repo_info['path'])) + "\\.git"
    git_folder = repo_path.replace('/', '\\')
    if os.path.exists(git_folder):
        cmd = f"""rmdir /q /s  {git_folder}"""
        output = subprocess.check_output(cmd, shell=True)

# remove files within folders
for root, dirnames, filenames in os.walk(cwd_repos):
    for filename in filenames:
        fp = os.path.join(root, filename)
        if not filename.endswith(extensions) and os.path.isfile(fp):
            try:
                os.remove(fp)
            except OSError as e:
                print("Error: %s - %s" % (e.filename, e.strerror))

# remove leftover empty folders
for root, dirnames, filenames in os.walk(cwd_repos):
    for dirname in dirnames:
        dir_path = os.path.join(root, dirname)
        if os.path.isdir(dir_path) and len(os.listdir(dir_path)) == 0:
            try:
                os.rmdir(dir_path)
            except OSError as e:
                print("Error: %s - %s" % (e.filename, e.strerror))
