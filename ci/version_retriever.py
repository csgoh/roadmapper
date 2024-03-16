#!/usr/bin/python3

import importlib
import subprocess
import sys

# Insert path to roadmapper package in system path
git_repo_root = subprocess.Popen(['/bin/git', 'rev-parse', '--show-toplevel'], stdout=subprocess.PIPE) \
    .communicate()[0] \
    .rstrip() \
    .decode('utf-8')
sys.path.insert(1, git_repo_root)


def get_current_version() -> str:
    roadmapper_version_module = importlib.import_module("src.roadmapper.version")
    current_version = getattr(roadmapper_version_module, "__version__")
    return current_version


if __name__ == "__main__":
    print(get_current_version())
