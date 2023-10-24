#!/bin/env python3

import datetime as dt
import re
import subprocess
import tempfile
from pathlib import Path
from typing import Any, Callable, NamedTuple, TypeVar
import jinja2
import yaml
from bs4 import BeautifulSoup, Tag

T = TypeVar("T")

FRONT_MATTER_PATTERN = re.compile(r"(?s)---\s*\n(.*?)\n\s*---")


def not_none(x: T | None) -> T:
    if x is None:
        raise TypeError
    return x


class PostData(NamedTuple):
    timestamp: dt.datetime
    title: str
    slug: str
    tags: list[str]


def parse_frontmatter(data: dict[str, Any]) -> PostData:
    data = {k.lower(): v for k, v in data.items()}

    params = {}

    ts_iso: str = str(data["date"])

    post_date = dt.date.fromisoformat(ts_iso)
    post_dt = dt.datetime.combine(post_date, dt.time.min)

    params["timestamp"] = post_dt

    params["title"] = data["title"]
    params["slug"] = data["slug"]

    params["tags"] = data.get("tags", [])

    return PostData(**params)


def extract_frontmatter(md_text: str) -> tuple[PostData, str]:
    match = FRONT_MATTER_PATTERN.search(md_text)
    if match is None:
        raise Exception("No front matter block could be found")

    content = match.group(1)
    fm_data: dict[str, Any] = yaml.safe_load(content)
    fm_parsed = parse_frontmatter(fm_data)

    # remove front matter block from the text
    text_remainder = FRONT_MATTER_PATTERN.sub("", md_text, count=1)

    return fm_parsed, text_remainder


def footnotes_to_asides(soup: BeautifulSoup) -> BeautifulSoup:
    footnotes_section = not_none(soup.find("section", role="doc-endnotes"))
    assert isinstance(footnotes_section, Tag)
    # locate all footnotes
    footnote_tags: list[Tag] = list(
        footnotes_section.find_all(
            "li", role="doc-endnote", id=lambda val: bool(val and val.startswith("fn"))
        )
    )

    for fn in footnote_tags:
        # find each footnote's ref in the text
        fn_id = fn.get("id")

        # remove backlink from footnote text
        not_none(fn.find("a", role="doc-backlink")).extract()

        fn_contents = fn.contents
        fn_origin_location = not_none(soup.find("a", href=f"#{fn_id}"))

        # find the parent paragraph of the reference

        origin_paragraph = not_none(fn_origin_location.find_parent("p"))

        # remove the original link
        fn_origin_location.extract()

        aside_tag = soup.new_tag("aside")
        aside_tag.extend(fn_contents)
        origin_paragraph.insert_after(aside_tag)

    # delete the footnotes section
    footnotes_section.decompose()

    return soup


class SiteBuilder:
    def __init__(
        self,
        output_dir: Path | str,
        templates_dir: Path | str,
        base_template_name: str = "base.html",
        posts_list_template_name: str = "posts_list.html",
        style: Path | str | None = None,
        overwrite: bool = True,
    ):
        self.posts_data: dict[str, PostData] = {}
        self.output_dir = Path(output_dir)
        self.templates_dir = Path(templates_dir)

        self.base_template_name = base_template_name
        self.posts_list_template_name = posts_list_template_name

        self.transformations: list[Callable[[BeautifulSoup], BeautifulSoup]] = []

        self.overwrite = overwrite

        self.template_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(self.templates_dir)
        )

        self._title_formatter: Callable[[str], str] | None = None

        self.style: str | None = None
        if style is not None:
            with open(Path(style), "r") as fp:
                self.style = fp.read()

    def add_transformations(self, *args):
        for a in args:
            self.transformations.append(a)

        return self

    @property
    def title_formatter(self) -> Callable[[str], str]:
        if self._title_formatter is None:
            return lambda x: x
        return self.title_formatter

    @title_formatter.setter
    def title_formatter(self, title_formatter: Callable[[str], str]):
        self.title_formatter = title_formatter

    def make_posts_list(self):
        pass

    def build_all_pages(self, input_dir: Path | str):
        pass

    def format_title(self, title: str):
        tf = self.title_formatter
        return tf

    def build_page(self, input_file: Path | str, page_title: str | None = None):
        with open(Path(input_file), "r") as fp:
            md_input = fp.read()

        template = self.template_env.get_template(self.base_template_name)
        meta, md_text = extract_frontmatter(md_input)

        if page_title is None:
            page_title = self.title_formatter(meta.title)

        if (s := meta.slug) in self.posts_data:
            exception_text = (
                f"The slug '{s}' for '{meta.title}'"
                + f" is already assocated with '{self.posts_data[s]}'."
                + "\nSlugs must be unique."
            )
            raise Exception(exception_text)

        self.posts_data[meta.slug] = meta

        html_text = markdown_to_html_pandoc(md_text)
        html_modifiers = self.transformations
        html_body = apply_transformations(html_text, html_modifiers)

        template_params = {"title": page_title, "content": html_body}

        if self.style is not None:
            template_params["style"] = self.style

        rendered_html = template.render(template_params)

        output_file = self.output_dir.joinpath(meta.slug).with_suffix(".html")
        if not self.overwrite and output_file.exists():
            raise FileExistsError(f"{output_file} already exists")

        with open(output_file, "w") as fp:
            fp.write(rendered_html)


def markdown_to_html_pandoc(md_text: str) -> str:
    tmp_file = Path(tempfile.gettempdir()).joinpath(tempfile.mktemp())
    try:
        with open(tmp_file, "w") as fp:
            fp.write(md_text)

        proc = subprocess.run(
            f"pandoc {str(tmp_file)} -f markdown -t html",
            shell=True,
            capture_output=True,
        )

        return proc.stdout.decode("utf-8")

    finally:
        tmp_file.unlink()


def apply_transformations(
    html_text: str,
    modifiers: list[Callable[[BeautifulSoup], BeautifulSoup]],
) -> str:
    soup = BeautifulSoup(html_text, "html.parser")

    for mod in modifiers:
        soup = mod(soup)

    container_tag = soup.new_tag("div")
    container_tag.attrs["class"] = "container"

    container_tag.extend(soup.contents)
    return container_tag.prettify()


def main():
    templates_dir = Path(__file__).parent.joinpath("templates")
    output_dir = Path(__file__).parent.joinpath("output")
    input_dir = Path(__file__).parent.joinpath("md")

    if not output_dir.exists():
        output_dir.mkdir()

    with open(input_dir.joinpath("post.md")) as fp:
        html = markdown_to_html_pandoc(fp.read())
        print(html)

    builder = SiteBuilder(
        output_dir=output_dir, templates_dir=templates_dir, style="./styles.css"
    )
    builder.add_transformations(footnotes_to_asides)
    builder.build_page(input_dir.joinpath("post.md"))


if __name__ == "__main__":
    main()
