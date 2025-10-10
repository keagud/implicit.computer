#!/usr/bin/env python3

import json
from pathlib import Path
import shutil
import os
import subprocess
from pprint import pprint


def get_root():
    return Path(__file__).parent.parent


def get_directory_bytes(path: Path) -> int:
    return sum(f.stat().st_size for f in Path(path).rglob("*") if f.is_file())


def get_git_hash():
    return (
        subprocess.run("git rev-parse --short HEAD", shell=True, stdout=subprocess.PIPE)
        .stdout.decode("utf-8")
        .strip()
    )


def main():
    public_dir = get_root().joinpath("public")
    quotes_file = public_dir.joinpath("quotes.json")

    with open(quotes_file, "r") as fp:
        quotes_json: dict = json.load(fp)

    size_kb = get_directory_bytes(public_dir) / 1024

    new_quotes = [
        f"{size_kb:.2f}"
    ]


    pprint(new_quotes)


if __name__ == "__main__":
    main()
