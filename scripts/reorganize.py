

from pathlib import Path

import shutil
import os
import datetime as dt


PREFIX_LEN = len("YYYY-MM-DD")



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

        shutil.copy2(f, month_dir)
        os.unlink(f)
        
    print(f"Copied {len(markdown_files)} posts" )

    




    pass

def main():
    root  = Path(__file__).parent

    dirs = [root.joinpath("content/blog"), root.joinpath( "content/notes")]


    reorg_dir(Path("content/blog"), "Posts")

    reorg_dir(Path("content/notes"), "Notes")

    pass

if __name__ == "__main__":
    main()
