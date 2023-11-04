#!/bin/bash


REPO_DIR=$(dirname "$0")
LOG_FILE="$REPO_DIR/watcher.log"


cd "$REPO_DIR" || return 1

# fetch updates
git fetch origin
if [ "$(git rev-parse HEAD)" != "$(git rev-parse origin/master)" ]; then
        echo "Changes were detected in the main repository"
        # Run the action for changes in the main repository here
fi

# fetch submodule updates
git submodule update --init --recursive

for submodule in $(git submodule status --recursive | awk '{print $2}'); do
    if [ "$(git -c $submodule rev-parse head)" != "$(git -c $submodule rev-parse origin/master)" ]; then
        echo "changes were detected in submodule: $submodule"
        # run the action for changes in this submodule here
    fi
done

# merge changes destructively
git merge --no-edit -X theirs origin/master

if [ $? -eq 0 ]; then
      # TODO  run the script to rebuild everything
        echo "Changes were merged destructively" && \
        echo "$(date) rebuilt all files"  >> "$LOG_FILE"
else
  echo "$(date) [nothing to do]"  >> "$LOG_FILE"
fi
