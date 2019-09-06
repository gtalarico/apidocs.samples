"""
Update Code Samples

Usage:
    python update.py
"""

import os
import json
import subprocess
from pathlib import Path
import shutil

with open('repos.json') as fp:
    repos = json.load(fp)

# shutil.rmtree("repos", ignore_errors=True)
# TODO could make it more efficient to update, but would requiring keeping .git/
# Not worth it at this point since rebuilding the entire thing only takes 1 min

for repo_info in repos:
    repo_path = repo_info['path']
    git_url = repo_info['url']
    if os.path.exists(repo_path):
        print(f'Already Exists - {repo_path}' )
        continue
    Path(repo_path).mkdir(parents=True, exist_ok=True)

    cmd = f"""
        git clone --depth=1 {git_url} {repo_path} \
        && rm -rdf {repo_path}/.git \
        && find repos -type f \( \
            ! -name "*.cs" \
            -and \
            ! -name "*.py" \
        \) -exec rm -rf "{{}}" \\;
    """
    output = subprocess.check_output(cmd, shell=True)
