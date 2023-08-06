from os import listdir, walk
from os.path import isfile, join
from datetime import datetime


def _get_files(path, type=None):
    if path.endswith("/"):
        path = path[:-1]
    files = []
    for (dirpath, dirnames, filenames) in walk(path):
        for file in filenames:
            files.append(f"{dirpath}/{file}")
    return files

def _unify_domain(path):
    result = ""
    for file in _get_files(path):
        with open(file, "r") as content:
            c = content.read().rstrip()
            if not c.endswith("\n"):
                c += "\n"
            c += "\n"
            result += c
    return result

def _generate_file(path, filename, content):
    if path.endswith("/"):
        path = path[:-1]
    with open(f"{path}/{filename}", "w+") as f:
        f.write(content)

def unify_domain(path="./domain", to=".", filename="domain.yml"): # pragma: no cover
    content = _unify_domain(path)
    _generate_file(to, filename, content)
    print("File domain.yml created successfully.")
    return "OK"
