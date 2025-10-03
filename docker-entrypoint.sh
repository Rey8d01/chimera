#!/usr/bin/env sh
set -e

# Set ENV to 'dev' if not already defined
ENV=${ENV:-dev}

case "$1" in
  web)
    shift
    echo "Starting web server in $ENV environment, DEBUG=$DEBUG..."

    echo "Applying SQLite migrations..."
    python /app/db/migrate_sqlite.py up

    UVICORN_LOG_LEVEL="info"
    if [ "$DEBUG" == "1" ]; then
      UVICORN_LOG_LEVEL="debug"
    fi
    UVICORN_ARGS=
    if [ "${ENV}" == "dev" ]; then
      UVICORN_ARGS="--reload --reload-dir /app/src"
    fi

    exec uvicorn asgi:web_app --no-server-header --workers 1 --host 0.0.0.0 --port 80 $UVICORN_ARGS --log-level $UVICORN_LOG_LEVEL
    ;;
  worker)
    shift
    echo "Celery worker is not implemented yet."
    # exec celery -A app.worker worker --loglevel=info "$@"
    ;;
  beat)
    shift
    echo "Celery beat is not implemented yet."
    # exec celery -A app.worker beat --loglevel=info "$@"
    ;;
  *)
    echo "Usage: $0 {web|worker|beat} [args]" >&2
    exit 1
    ;;
esac
