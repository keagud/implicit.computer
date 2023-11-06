from pathlib import Path
from flask import Flask, send_from_directory

app = Flask(__name__)

from definitions import OUTPUT_DIR, POSTS_HTML_DIR


@app.route("/")
def homepage():
    return send_from_directory(OUTPUT_DIR, "home.html")


@app.route("/blog/")
def posts_list():
    return send_from_directory(OUTPUT_DIR, "posts.html")


@app.route("/blog/<slug>")
def blogpost(slug):
    return send_from_directory(POSTS_HTML_DIR, f"{slug}.html")


@app.route("/resume")
def resume():
    return send_from_directory(OUTPUT_DIR, "resume.html")
