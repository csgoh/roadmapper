#!/usr/bin/python3

import os.path
import subprocess
import sys

import version_retriever


def update_version(new_version: str, version_file: str):
    current_version = version_retriever.get_current_version()
    path_to_version_file = get_absolute_path_to_version_file(version_file)
    replace_current_with_new_version(current_version, new_version, path_to_version_file)


def get_absolute_path_to_version_file(version_file: str):
    git_repo_root = subprocess.Popen(['/bin/git', 'rev-parse', '--show-toplevel'], stdout=subprocess.PIPE) \
        .communicate()[0] \
        .rstrip() \
        .decode('utf-8')
    path_to_version_file = os.path.join(git_repo_root, version_file)
    return path_to_version_file


def replace_current_with_new_version(current_version, new_version, path_to_version_file):
    with open(path_to_version_file, "r") as version_file:
        file_data = version_file.read()
    updated_file_data = file_data.replace(current_version, new_version)
    with open(path_to_version_file, "w") as version_file:
        version_file.write(updated_file_data)


if __name__ == "__main__":
    new_version = sys.argv[1]
    version_file = "src/roadmapper/version.py"
    update_version(new_version, version_file)

    print(f"Version in `{version_file}` updated to `{new_version}`")
