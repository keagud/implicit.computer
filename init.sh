#!/bin/bash

# start the cron daemon
service cron start

# start the web server
# query for the number of available cpus
CPUS=$(nproc --all)

# start with 2 workers per cpu
gunicorn -w $(( CPUS * 2 )) -b 0.0.0.0:8000 site_src:app 



