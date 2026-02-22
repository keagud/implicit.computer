

from pathlib import Path


from pre_build import extract_metadata
import shutil
import os
import datetime as dt

import toml

PREFIX_LEN = len("YYYY-MM-DD")
ROOT_DIR = Path(__file__).parent.parent.resolve()



def write_index_toml(title: str, dir: Path):
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

def insert_alias(content:str , alias_dir: Path | str) -> str:


    metadata = extract_metadata(content)

    if metadata is None:
        raise Exception(f"No metadata found")

    parsed_metadata = toml.loads(metadata)

    slug = parsed_metadata["slug"]

    alias_path = f"{alias_dir}/{slug}"


    aliases_line = f'aliases = ["{alias_path}"]'
    content_lines = content.strip().splitlines()

    content_lines.insert(1, aliases_line)
    return "\n".join(content_lines)


def reorg_dir(dir: Path, label_plural: str):
    dir = dir.resolve()
    markdown_files = [f for f in  dir.glob("*.md") if not f.name.startswith('_')]
    for f in markdown_files:

        post_date = dt.date.fromisoformat(f.name[:PREFIX_LEN])

        y = post_date.strftime("%Y")
        m = post_date.strftime("%m")
        d = post_date.strftime("%d")

        month_name = post_date.strftime("%B").title()

        month_dir = dir.joinpath(f"{y}/{m}")
        month_dir.mkdir(exist_ok=True, parents=True)


        year_dir = month_dir.parent

        write_index_toml(f"{label_plural} from {y}", year_dir)
        write_index_toml(f"{label_plural} from {month_name} {y}", month_dir)


        with open(f, "r") as fp:
            file_content = insert_alias(fp.read(), str(f.parent.name))

        new_path = month_dir.joinpath(f.name)

        with open(new_path, "w") as fp:
            fp.write(file_content)

        os.unlink(f)
        
    print(f"Copied {len(markdown_files)} posts" )

    




    pass

def main():

    posts_dir = ROOT_DIR.joinpath("content/blog")
    notes_dir = ROOT_DIR.joinpath("content/notes")

    reorg_dir(posts_dir, "Posts")
    reorg_dir(notes_dir, "Notes")


if __name__ == "__main__":
    main()
