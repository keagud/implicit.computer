#!/bin/sh

# start cron daemon as a background job
crond -b -d 0 -L /site/cron.log &

# start web server
static-web-server --port "$env_port" -d ./public
