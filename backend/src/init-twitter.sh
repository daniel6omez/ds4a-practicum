#!/bin/bash
set -e
echo 'Starting cron jobs'
nohup gunicorn --bind 0.0.0.0:8080 -t 100000 app:server >> /var/log/gunicorn.log 2>&1 &
cron -f

