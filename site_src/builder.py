#!/bin/env python3
from shutil import copytree
import json
from tempfile import TemporaryDirectory
import datetime as dt
from dataclasses import dataclass, field
import re
import subprocess
import tempfile
from pathlib import Path
from typing import Any, Callable, NamedTuple, TypeVar
import jinja2
import yaml
from bs4 import BeautifulSoup, Tag

from .Resume.render import build_resume

T = TypeVar("T")

from definitions import (
    POSTS_HTML_DIR,
    POSTS_MARKDOWN_DIR,
    ROOT_DIR,
    STATIC_DIR,
    STYLES_DIR,
    ASSETS_DIR,
    TEMPLATE_DIR,
    OUTPUT_DIR,
)

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
    footnotes_section = soup.find(role="doc-endnotes")

    if footnotes_section is None:
        return soup
    assert isinstance(footnotes_section, Tag)
    # locate all footnotes
    footnote_tags: list[Tag] = list(
        footnotes_section.find_all(id=lambda val: bool(val and val.startswith("fn")))
    )



    for fn in footnote_tags:
        # find each footnote's ref in the text
        fn_id = fn.get("id")

        # remove backlink from footnote text
        not_none(fn.find("a", role="doc-backlink")).extract()


        for t in fn.find_all("p"):
            t.name = "span"

        fn_contents = fn.contents
        fn_origin_location = not_none(soup.find("a", href=f"#{fn_id}"))

        fn_label = soup.new_tag(
            "label", attrs={"class": "margin-toggle sidenote-number", "for": fn_id}
        )

        fn_checkbox = soup.new_tag(
            "input", attrs={"id": fn_id, "class": "margin-toggle", "type": "checkbox"}
        )

        fn_content_span = soup.new_tag(
            "span", attrs={"class": "note-right note sidenote"}
        )

        fn_footnote_p = soup.new_tag("span", attrs={"class": "footnote-p"})
        fn_footnote_p.extend(fn_contents)

        fn_content_span.append(fn_footnote_p)

        fn_all_span = soup.new_tag("span")
        fn_all_span.extend([fn_label, fn_checkbox, fn_content_span])

        fn_origin_location.replace_with(fn_all_span)

    footnotes_section.decompose()

    return soup


@dataclass(kw_only=True)
class BuildConfig:
    output_dir: Path = POSTS_HTML_DIR
    assets_dir: Path = ASSETS_DIR
    templates_dir: Path = TEMPLATE_DIR
    posts_md_dir: Path = POSTS_MARKDOWN_DIR
    styles_dir: Path = STYLES_DIR
    static_dir: Path = STATIC_DIR
    base_template_name: str = "base.html"
    post_template_name: str = "post.html"
    static_page_template_name: str = "static_page.html"
    posts_list_template_name: str = "posts_list.html"
    style_files: list[str] = field(default_factory=lambda: [])

    overwrite: bool = True
    exclude_upcoming: bool = True
    transformations: list[Callable[[BeautifulSoup], BeautifulSoup]] = field(
        default_factory=lambda: []
    )

    def add_transformations(self, *args):
        for a in args:
            self.transformations.append(a)

        return self


class SiteBuilder:
    def __init__(self, config: BuildConfig, style_files: list[str] = []):
        self.config = config
        self.posts_data: dict[str, PostData] = {}
        self.style_files = style_files

        self.output_dir = Path(config.output_dir)
        self.templates_dir = Path(config.templates_dir)
        self.styles_dir = Path(config.styles_dir)

        self.transformations: list[Callable[[BeautifulSoup], BeautifulSoup]] = []

        self.template_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(self.templates_dir)
        )

        self._title_formatter: Callable[[str], str] | None = None

        self.template_args = {}

        self.styles: str | None = None

        if config.styles_dir.exists():
            styles_block = []
            for f in config.styles_dir.glob("*.css"):
                if not f.name in self.config.style_files:
                    continue
                with open(f, "r") as fp:
                    styles_block.append(fp.read())

            self.styles = "\n".join(styles_block)
            self.template_args["style"] = self.styles

        if (json_path := self.config.assets_dir.joinpath("quotes.json")).exists():
            with open(json_path, "r") as fp:
                json_data = json.load(fp)

            quotes_literals = ", ".join([rf'"{q}"' for q in json_data["quotes"]])
            quotes = f"[{quotes_literals}]"

            self.template_args["quotes"] = quotes

    @property
    def title_formatter(self) -> Callable[[str], str]:
        if self._title_formatter is None:
            return lambda x: x
        return self.title_formatter

    @title_formatter.setter
    def title_formatter(self, title_formatter: Callable[[str], str]):
        self.title_formatter = title_formatter

    def build_static(self, page_title: str, page_name: str):
        """Insert static HTML content (like the homepage) into the base template"""

        with open(self.config.static_dir.joinpath(page_name), "r") as fp:
            input_content = fp.read()

        page_template = self.template_env.get_template(
            self.config.static_page_template_name
        )

        render_params = self.template_args | {
            "title": page_title,
            "content": input_content,
        }

        rendered = page_template.render(render_params)

        output_file = self.config.output_dir.joinpath(page_name).with_suffix(".html")
        with open(output_file, "w") as fp:
            fp.write(rendered)

        return output_file

    def make_posts_list(
        self, page_title: str | None = None, page_name: str = "posts.html"
    ):
        template_data = {
            "posts_list": sorted(
                list(self.posts_data.values()), key=lambda p: p.timestamp, reverse=True
            )
        }

        if page_title is None:
            page_title = self.title_formatter("All Posts")

        posts_list_template = self.template_env.get_template(
            self.config.posts_list_template_name
        )

        posts_list_rendered = posts_list_template.render(
            self.template_args | template_data
        )

        filepath = self.output_dir.joinpath(page_name)
        with open(filepath, "w") as fp:
            fp.write(posts_list_rendered)

        return filepath

    def build_all_pages(self, dir_name: str = "posts") -> list[Path]:
        input_dir = Path(self.config.posts_md_dir)

        page_paths = []
        for page in input_dir.glob("*.md"):
            page_path = self.build_page(page, dir_name=dir_name)
            if page_path is not None:
                page_paths.append(page_path)

        return page_paths

    def build_page(
        self,
        input_file: Path | str,
        page_title: str | None = None,
        dir_name: str = "posts",
    ) -> Path | None:
        with open(Path(input_file), "r") as fp:
            md_input = fp.read()

        template = self.template_env.get_template(self.config.post_template_name)
        meta, md_text = extract_frontmatter(md_input)

        output_file = self.output_dir.joinpath(f"{dir_name}/{meta.slug}").with_suffix(
            ".html"
        )
        # technically a post queue system
        if self.config.exclude_upcoming and meta.timestamp > dt.datetime.now():
            return

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
        html_modifiers = self.config.transformations
        html_body = apply_transformations(html_text, html_modifiers)

        template_params = {"title": page_title, "content": html_body}

        if self.styles is not None:
            template_params.update({"style": self.styles})

        rendered_html = template.render(template_params)

        output_dir = self.output_dir.joinpath(dir_name)
        output_dir.mkdir(exist_ok=True)

        output_file = self.output_dir.joinpath(f"{dir_name}/{meta.slug}").with_suffix(
            ".html"
        )
        if not self.config.overwrite and output_file.exists():
            raise FileExistsError(f"{output_file} already exists")

        with open(output_file, "w") as fp:
            fp.write(rendered_html)

        return output_file


def markdown_to_html_pandoc(md_text: str) -> str:
    tmp_file = Path(tempfile.gettempdir()).joinpath(tempfile.mktemp())
    try:
        with open(tmp_file, "w") as fp:
            fp.write(md_text)

        proc = subprocess.run(
            f"pandoc {str(tmp_file)} -f markdown+fenced_code_attributes -t html",
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


def build_all(output_dir: Path):
    with TemporaryDirectory() as build_dir_str:
        build_dir = Path(build_dir_str).joinpath("build")
        build_dir.mkdir()

        config = BuildConfig(
            output_dir=build_dir,
            style_files=["style.css"],
            transformations=[footnotes_to_asides],
        )

        page_paths: list[Path] = []

        builder = SiteBuilder(config)
        post_paths = builder.build_all_pages()
        page_paths.extend(post_paths)

        posts_list_path = builder.make_posts_list()
        page_paths.append(posts_list_path)

        static_files = [
            {"page_title": "Home", "page_name": "home.html"},
            {"page_title": "About", "page_name": "about.html"},
        ]

        for f in static_files:
            filepath = builder.build_static(**f)
            page_paths.append(filepath)

        copytree(build_dir, output_dir, dirs_exist_ok=True)


def main():
    output_dir = Path(__file__).parent.joinpath("output")
    input_dir = Path(__file__).parent.joinpath("md")
    assets_dir = Path(__file__).parent.joinpath("assets")

    if not output_dir.exists():
        output_dir.mkdir()

    with open(input_dir.joinpath("post.md")) as fp:
        html = markdown_to_html_pandoc(fp.read())

    builder = cfg = BuildConfig(
        output_dir=output_dir,
        assets_dir=assets_dir,
        style_files=["style.css"],
        transformations=[footnotes_to_asides],
    )

    builder = SiteBuilder(cfg)
    builder.build_page(input_dir.joinpath("post.md"))

    builder.make_posts_list()


if __name__ == "__main__":
    main()
