#!/bin/bash


REPO_DIR=$(dirname "$0")
LOG_FILE="$REPO_DIR/watcher.log"


cd "$REPO_DIR" || return 1

# fetch updates
git fetch origin
if [ "$(git rev-parse HEAD)" != "$(git rev-parse origin/master)" ]; then

        # merge changes destructively
        git merge --no-edit -X theirs origin/master

        #build the site
        python3 "$REPO_DIR/build_site.py"

        echo "$(date) rebuilt all files"  >> "$LOG_FILE"

fi


if [  "$(git -c Resume rev-parse head)" != "$(git -C Resume rev-parse origin/master)" ]; then

  # fetch updates from submodule and build
  git submodule update --init --recursive --remote
  python3 "$REPO_DIR/build_resume.py"


  echo "$(date) updated resume"  >> "$LOG_FILE"
fi


