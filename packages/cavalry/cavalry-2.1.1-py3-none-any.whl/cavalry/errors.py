import sys


def err(msg, code):
    if code > 0:
        sys.stderr.write(msg + "\n")
        sys.exit(code)
    else:
        sys.stdout.write(msg + "\n")


def missing_secrets_file(file):
    err(f"Unable to find secrets file at {file}", 1)


def missing_project(project):
    err(f"Project {project} not found", 2)


def missing_key(project, key):
    err(f"Key {key} in {project} not found", 3)
