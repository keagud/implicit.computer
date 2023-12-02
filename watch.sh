#!/bin/bash

echo "$(date) Started" >> /var/log/site_messages

SCRIPT_DIR=$( readlink -f .)
VENV_PATH="$SCRIPT_DIR/.venv/bin"
REQS_PATH="$SCRIPT_DIR/requirements.txt"
RESUME_REQS_PATH="$SCRIPT_DIR/Resume/requirements.txt"

OUTPUT_DIR="/home/user/html"

SITE_DIR="/var/www/implicit.computer/html"

eval "$VENV_PATH/pip install -r $REQS_PATH"
eval "$VENV_PATH/pip install -r $RESUME_REQS_PATH"

mkdir -p "$OUTPUT_DIR" || exit
eval "SITE_OUTPUT_DIR=$OUTPUT_DIR $VENV_PATH/python3 builder.py force" 2>> /var/log/site_messages 


if [ ! -L "$SITE_DIR" ]; then
  ln -s "$OUTPUT_DIR" "$SITE_DIR"
fi

echo "$(date) Ran successfully" >> /var/log/site_messages

