#!/usr/bin/env python3

import json
import os
import subprocess
from pathlib import Path

CONFIG_PATH = Path("./watch-config.json")

def poll_repo(remote: str, local: str | Path, branch: str | None = None) -> bool:
    local = Path(local)

    if branch is None:
        branch = "master"
    original_cwd = Path.cwd()
    try:

        # case: no local clone exists
        if not local.joinpath(".git").exists():
            local.mkdir(parents=True, exist_ok=True)
            subprocess.run(
                f"git clone --recurse-submodules --remote-submodules --branch {branch} --single-branch {remote} {local.as_posix()}",
                shell=True,
            ).check_returncode()
            return True

        os.chdir(local)

        subprocess.run(["git", "submodule", "update", "--init", "--recursive"]).check_returncode()
        subprocess.run(["git", "fetch"]).check_returncode()

        result = subprocess.run(
            'echo "$(git rev-parse @) $(git rev-parse @{u})"',
            shell=True,
            capture_output=True,
        )

        local_head, remote_head = result.stdout.decode("utf-8").strip().split()

        # case: remote and local heads are the same, nothing to do
        if local_head == remote_head:
            return False

        # case: remote and local differ, should be merged
        subprocess.run("git reset --hard origin/master".split()).check_returncode()

        return True

    finally:
        os.chdir(original_cwd)


def main():

    with open(CONFIG_PATH, "r") as fp:
        config_entries = json.load(fp)

    config_vals = [(d["remote"], d["local"], d["on_change"], d.get("branch")) for d in config_entries]

    for remote, local, on_change, branch in config_vals:
        if poll_repo(remote, local, branch):
            subprocess.run(on_change, shell=True, cwd=Path(local)).check_returncode()


if __name__ == "__main__":
    main()
