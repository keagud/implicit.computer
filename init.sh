#!/bin/bash

SCRIPT_DIR=$(dirname "$0")
WATCH_SCRIPT="$SCRIPT_DIR/watch.sh"

CRON_JOB="*/1 * * * * sh $WATCH_SCRIPT" 

echo "$CRON_JOB" > /tmp/crontab.txt  && crontab /tmp/crontab.txt

