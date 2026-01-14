#!/usr/bin/env python3

import json
from pathlib import Path
import shutil
import os
import subprocess
from pprint import pprint
from math import floor
from string import ascii_lowercase
import random


FILE_SIZE_BENCHMARKS_BYTES = {"Doom (1993)": 25772, "english wikipedia": 213964533268}


def get_root():
    return Path(__file__).parent.parent


def format_float(x):
    return f"{round(x, 2):.1f}".rstrip("0").rstrip(".")


def get_mult_label(mult: float, label: str, factor: int = 10_000):
    if mult == 1:
        return f"Exactly the size of {label}!"
    use_scientific = mult >= factor or mult <= (1 / factor)
    inverse = floor(1 / mult)

    if mult < 1 and use_scientific:
        return f"~1/{inverse:g} the size of {label}!"

    elif mult > 1 and use_scientific:
        return f"{mult:g}x the size of {label}!"

    else:
        return f"~{format_float(mult)}x the size of {label}!"


def compare_filesizes(bytes_self: int, bytes_other: int, label: str):
    mult = bytes_self / bytes_other
    return get_mult_label(mult, label)


def get_directory_bytes(path: Path) -> int:
    return sum(f.stat().st_size for f in Path(path).rglob("*") if f.is_file())


def merge_dicts(d1: dict[str, int], d2: dict[str, int]) -> dict[str, int]:
    all_keys = set(d1.keys()).union(set(d2.keys()))

    merged = {k: 0 for k in all_keys}
    for k in all_keys:
        merged[k] += d1.get(k, 0)
        merged[k] += d2.get(k, 0)

    return merged


def get_file_letter_counts(filepath: Path):
    results = {letter: 0 for letter in ascii_lowercase}
    with open(filepath, "r") as fp:
        text = fp.read().lower()

    for letter in ascii_lowercase:
        results[letter] += text.count(letter)

    return results


def get_total_letter_counts(root_path: Path):
    all_markdown = (f for f in root_path.rglob("*.md") if f.is_file())

    total_results = {letter: 0 for letter in ascii_lowercase}

    for f in all_markdown:
        results = get_file_letter_counts(f)
        total_results = merge_dicts(total_results, results)

    return total_results


def get_git_hash():
    try:
        return (
            subprocess.run(
                "git rev-parse --short HEAD",
                shell=True,
                stdout=subprocess.PIPE,
                check=True,
            )
            .stdout.decode("utf-8")
            .strip()
        )

    except Exception as _:
        return None


def make_file_comparison_quotes():
    public_dir = get_root().joinpath("public")

    size_bytes = get_directory_bytes(public_dir)

    size_mb = size_bytes / 1048576
    new_quotes = [f"{size_mb:.1f} megabytes!"]

    for label, compare_size in FILE_SIZE_BENCHMARKS_BYTES.items():
        comparison_text = compare_filesizes(size_bytes, compare_size, label)
        new_quotes.append(comparison_text)

    return new_quotes


def make_letter_count_quotes():
    content_dir = get_root().joinpath("content")

    letter_counts = get_total_letter_counts(content_dir)
    letter_data = sorted(
        [(k, v) for k, v in letter_counts.items()], key=lambda t: t[1], reverse=True
    )

    selected = [
        letter_data[0],
        letter_data[floor(len(letter_data) * 0.25)],
        letter_data[floor(len(letter_data) * 0.5)],
        letter_data[floor(len(letter_data) * 0.75)],
        letter_data[-1],
        random.choice(letter_data),
        random.choice(letter_data)
    ]

    return [f"contains {c} '{l}'s!" for l, c in set(selected)]


def main():
    public_dir = get_root().joinpath("public")
    quotes_file = public_dir.joinpath("quotes.json")

    with open(quotes_file, "r") as fp:
        quotes_json: dict = json.load(fp)

    size_bytes = get_directory_bytes(public_dir)
    print(size_bytes)

    size_mb = size_bytes / 1048576

    new_quotes = []

    if (git_hash := get_git_hash()) is not None:
        comment = f"You're reading commit {git_hash}!"
        new_quotes.append(comment)

    new_quotes.extend(make_letter_count_quotes())
    new_quotes.extend(make_file_comparison_quotes())

    pprint(new_quotes)
    quotes_json["quotes"].extend(new_quotes)

    with open(quotes_file, "w") as fp:
        json.dump(quotes_json, fp)


if __name__ == "__main__":
    main()
