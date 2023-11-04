#!/bin/env python3 

from definitions import ROOT_DIR, OUTPUT_DIR
from shutil import copyfile
from site_src import build_all, build_resume


if __name__ == "__main__":
    html_path = build_resume("html")
    pdf_path = build_resume("pdf")

    copyfile(html_path, OUTPUT_DIR.joinpath("resume.html"))
    copyfile(pdf_path, OUTPUT_DIR.joinpath("resume.pdf"))
