#!/usr/bin/env python3

import datetime as dt
from pathlib import Path
import sys
import re
from typing import Callable, List
from pprint import pprint


HEADER_REGEX = r'^\+\+\+\n(.*?)\n\+\+\+'


def get_root():
    return Path(__file__).parent.parent


def extract_metadata(content: str):
    
    match = re.search(HEADER_REGEX, content, re.MULTILINE | re.DOTALL)
    
    if match:
        return match.group(1)
    return None


def find_first[T](fn: Callable[[T], bool], list: List[T]) -> T | None:
    for i in list:
        if fn(i):
            return i
    return None
        


def mark_future_posts_as_draft(root_dir: Path):
    post_files = root_dir.rglob("*.md")

    today = dt.date.today()
    changes_count = 0

    for post_file in post_files:

        with open(post_file, 'r') as fp:
            content = fp.read()

        header = extract_metadata(content)
        if header is None:
            continue

        header_lines = [ ln.strip() for ln in header.split('\n')]

        # find the date in the TOML metadata
        post_date_line = find_first(lambda x: re.match(r'date\s*=', x) is not None, header_lines)

        # if no date specified, nothing to do
        if post_date_line is None:
            continue


        # raises an exception on failure
        # (by design - don't want to continue with the build if the date is invalid)
        post_date = dt.date.fromisoformat(post_date_line.split('=')[-1].strip())

        # if the post date is in the past, nothing to do
        if post_date <= today:
            continue


        # if there's an existing draft status, update it to be 'true'
        # otherwise append as the last line
        if current_draft_line := find_first(lambda x: re.match(r'draft\s*=\s*', x) is not None, header_lines) is not None:
            draft_line_index = header_lines.index(current_draft_line)
            header_lines[draft_line_index] = "draft = true"

        else:
            header_lines.append("draft = true")



        updated_header = "\n".join(["+++"] + header_lines + ["+++"])


        updated_content = re.sub(HEADER_REGEX, updated_header, content, flags = re.MULTILINE | re.DOTALL)

        with open(post_file, "w") as fp:
            fp.write(updated_content)

        changes_count += 1
        print(f"Marked post {post_file} as draft, to be published {post_date.isoformat()}")

    print(f"Marked {changes_count} posts as draft")


def main():
    content_dir = get_root().joinpath('content')
    mark_future_posts_as_draft(content_dir)


if __name__ == "__main__":
    main()
