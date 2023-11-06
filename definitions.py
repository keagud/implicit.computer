from pathlib import Path
from typing import Final

import subprocess


ROOT_DIR: Final = Path(__file__).parent
OUTPUT_DIR = ROOT_DIR.joinpath("_output")
ASSETS_DIR: Final = ROOT_DIR.joinpath("assets")
TEMPLATE_DIR: Final = ASSETS_DIR.joinpath("templates")
STYLES_DIR: Final = ASSETS_DIR.joinpath("css")
POSTS_MARKDOWN_DIR = ROOT_DIR.joinpath("md")

STATIC_DIR = ASSETS_DIR.joinpath("static")
RESUME_DIR = ROOT_DIR.joinpath("Resume")

POSTS_HTML_DIR = OUTPUT_DIR.joinpath("posts")

_get_blog_repo_url = subprocess.run(
    r"git config --get remote.origin.url", capture_output=True, shell=True
)

_get_blog_repo_url.check_returncode()

BLOG_REPO_URL: Final = _get_blog_repo_url.stdout.decode("UTF-8")
RESUME_REPO_URL: Final = "https://github.com/keagud/Resume.git"
