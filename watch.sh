#!/bin/bash


VENV_PATH="./.venv/bin/python3"
OUTPUT_DIR="$1"

SITE_DIR="/var/www/implicit.computer/html/"

mkdir -p "$OUTPUT_DIR" || exit
"$VENV_PATH/python3 builder.py all" || exit


if [ ! -L "$SITE_DIR/posts" ]; then
  ln -s "$OUTPUT_DIR" "$SITE_DIR/posts"
fi





