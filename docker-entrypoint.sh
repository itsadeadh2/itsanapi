#!/bin/sh

# Health check function using ping
healthcheck() {
  HOST=$1
  MAX_ATTEMPTS=10
  WAIT_TIME=10

  for attempt in $(seq 1 $MAX_ATTEMPTS); do
    if ping -c 1 $HOST > /dev/null 2>&1; then
      echo "Health check passed!"
      return 0
    else
      echo "Health check failed (attempt $attempt/$MAX_ATTEMPTS). Retrying in $WAIT_TIME seconds..."
      sleep $WAIT_TIME
    fi
  done

  echo "Health check failed after $MAX_ATTEMPTS attempts."
  return 1
}

# Perform health check
HEALTHCHECK_HOST="postgres.itsanapi-ecs.local"

if healthcheck $HEALTHCHECK_HOST; then
  python manage.py migrate
  python manage.py collectstatic --noinput

  exec gunicorn --bind 0.0.0.0:80 "itsanapi.wsgi:application" \
    --access-logfile - \
    --error-logfile - \
    --log-level $LOG_LEVEL
else
  echo "Application did not start due to failed health check."
  exit 1
fi
