#!/bin/bash

git submodule update --init --recursive --remote || exit

SCRIPT_DIR=$(dirname -- $(readlink -f  "$0") )
WATCH_SCRIPT="$SCRIPT_DIR/watch.sh"

CRON_JOB="*/1 * * * * root  cd $SCRIPT_DIR && sh $WATCH_SCRIPT &>> /var/log/site_messages" 

echo "$CRON_JOB" > /etc/cron.d/site_watch || exit

chmod +rw /etc/cron.d/site_watch
chown root:root /etc/cron.d/site_watch

