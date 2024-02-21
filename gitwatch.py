import json
import os
import subprocess
from pathlib import Path

CONFIG_PATH = Path("./watch-config.json")

def poll_repo(remote: str, local: str | Path) -> bool:
    local = Path(local)
    original_cwd = Path.cwd()
    try:

        # case: no local clone exists
        if not local.joinpath(".git").exists():
            local.mkdir(parents=True, exist_ok=True)
            subprocess.run(
                f"git clone --branch master --single-branch {remote} {local.as_posix()}",
                shell=True,
            ).check_returncode()
            return True

        os.chdir(local)
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

    config_vals = [(d["remote"], d["local"], d["on_change"]) for d in config_entries]

    for remote, local, on_change in config_vals:
        if poll_repo(remote, local):
            subprocess.run(on_change, shell=True).check_returncode()


if __name__ == "__main__":
    main()
