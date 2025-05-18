#!/bin/env python3

from pathlib import Path
import re
import tomllib
import json
import datetime as dt

FRONTMATTER_PATTERN = re.compile(r"^\+\+\+\n(.*?)\n\+\+\+", re.DOTALL)


def convert_post(post_path: Path):
    with open(post_path, "r") as fp:
        post_content = fp.read()

    m = FRONTMATTER_PATTERN.search(post_content)

    if m is None:
        print(f"Unable to find frontmatter for {post_path.as_posix()}")
        return

    fm = tomllib.loads(m.group(1))

    if (taxonomies := fm.get("taxonomies")) is not None:
        if (tags := taxonomies.get("tags")) is not None:
            fm["tags"] = tags
        del fm["taxonomies"]

    if (d := fm.get("date")) is not None:
        fm["date"] = d.isoformat()

    slug = fm["slug"]
    fm["permalink"] = f"/blog/{slug}.html"
    del fm["slug"]


    fm["layout"] = "post.html"

    fm_json = json.dumps(fm, indent=4)

    new_frontmatter = "\n".join(["---json", fm_json, "---"])

    modified_content = FRONTMATTER_PATTERN.sub(new_frontmatter, post_content)

    with open(post_path, "w") as fp:
        fp.write(modified_content)

    print(f"Modified {post_path.as_posix()}")


def main():
    posts_dir = Path(__file__).parent.joinpath("posts").resolve()
    print(posts_dir.as_posix())

    for post_path in posts_dir.glob("*.md"):
        convert_post(post_path)


if __name__ == "__main__":
    main()
