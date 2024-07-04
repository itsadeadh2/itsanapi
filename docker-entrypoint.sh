#!/bin/sh

cd src

exec gunicorn --bind 0.0.0.0:80 "app:create_app()"\
    --access-logfile - \
    --error-logfile - \
    --log-level $LOG_LEVEL