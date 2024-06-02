#!/bin/env python3


from pathlib import Path
import datetime as dt
import subprocess
import sys

LOCAL_PATH=Path("/var/site/")
REPO_URL = "https://github.com/keagud/implicit.computer.git"
LOCAL_PATH.mkdir(parents=True, exist_ok=True)

def update_last_changed():
    with open(LOCAL_PATH.joinpath("updated"), 'w') as fp:
        fp.write(dt.datetime.now().isoformat())

def main():

    head_file =  LOCAL_PATH.joinpath(".git/refs/heads/master")
    if head_file.exists():
        old_head = open(head_file, "r").read().strip()
        res = subprocess.run("git reset HEAD --hard && git pull", shell=True, cwd=LOCAL_PATH)
        res.check_returncode()

        new_head = open(head_file, "r").read().strip()
        if new_head == old_head:
            subprocess.run('logger -t "check-updates" "No changes to remote"', shell=True)
            sys.exit(0)

    else:
        subprocess.run(f"git clone {REPO_URL} {LOCAL_PATH.as_posix()}", shell=True).check_returncode()

        subprocess.run(f"git submodule update --init", shell=True, cwd=LOCAL_PATH).check_returncode()

    update_last_changed()


if __name__ == "__main__":
    main()
