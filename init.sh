#!/bin/sh


(crontab -l -u user 2>/dev/null; echo "*/5 * * * * * /home/user/site/") | crontab -u user


