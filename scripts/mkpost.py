#!/usr/bin/env python3

from collections.abc import Callable
import toml
from pathlib import Path
import datetime as dt
from sys import exit, argv
from os import environ
import subprocess
import argparse


from common import ROOT_DIR




def write_index_toml(title: str, dir: Path):
    if not dir.exists():
        dir.mkdir(exist_ok=True, parents=True)

    path = dir.joinpath("_index.md")
    if path.exists():
        return
    with open(path, "w") as fp:
        fp.write(make_index_toml(title))

def make_index_toml(title: str):
    return f"""
    +++
    title = "{title}"
    sort_by = "date"
    template = "posts-list.html"
    transparent = true
    +++

    """.strip()



def slugify(text):
    text = "".join(char if char.isalnum() else " " for char in text.lower())
    return "-".join(text.split())


def try_until[T](prompt: str, fn: Callable[[str], T]) -> T:
    while True:
        try:
            value = input(prompt).strip()
            return fn(value)
        except Exception as e:
            print(str(e))
            continue


def _raise(msg: str):
    raise Exception(msg)


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--type',choices=['note', 'post'], default='post')
    parser.add_argument('-e', '--edit', action='store_true')


    args = parser.parse_args()

    is_note = args.type == "note"
    section = "notes" if is_note else "blog"
    do_edit: bool = args.edit


    section_dir = ROOT_DIR.joinpath("content", section)

    title = try_until("Title: ", lambda s: s if s else _raise("A title is required"))
    default_slug = slugify(title)

    slug = try_until(
        f"Slug ({default_slug}): ",
        lambda s: (
            _raise("Invalid slug") if not all(c.isalnum() or c == "-" for c in s) else s
        ),
    )

    if not slug:
        slug = default_slug

    redirect_path = f"{section}/{slug}"

    today = dt.date.today()
    date = try_until(
        f"ISO-8601 date ({today}): ",
        lambda s: today if not s else dt.date.fromisoformat(s),
    )

    tags = [w for w in input("Tags (comma-separated): ").strip().split(",") if w]

    frontmatter = {
        "title": title,
        "slug": slug,
        "date": date,
        "aliases" : [ redirect_path ]
    }


    if tags:
        frontmatter["taxonomies"] = {"tags": tags}

    target_file = Path(f"{date.isoformat()}_{slug}.md")

    year_dirname = date.strftime("%Y")
    month_dirname = date.strftime("%m")


    month_name = date.strftime("%B").title()



    target_filepath_full = section_dir.joinpath(year_dirname,  month_dirname, target_file)

    if target_filepath_full.exists():
        print(f"{target_filepath_full} already exists")
        exit(1)


    label_plural = "Notes" if is_note else "Posts"

    month_dir = target_filepath_full.parent
    year_dir = month_dir.parent

    write_index_toml(f"{label_plural} for {month_name} {year_dirname}", month_dir)

    write_index_toml(f"{label_plural} for {year_dirname}", year_dir)

    frontmatter_str = "\n".join(
        [
            "+++",
            toml.dumps(frontmatter).strip(),
            "+++\n\n",
        ]
    )

    with open(target_filepath_full, "w") as fp:
        fp.write(frontmatter_str)

    print(f"Created '{target_file.as_posix()}'")


    if do_edit:
        editor_path = environ.get("EDITOR")
        if not editor_path:
            exit(0)
        editor_path = Path(editor_path).resolve()
        editor = editor_path.name
        return subprocess.run([editor, target_file])


if __name__ == "__main__":
    main()
