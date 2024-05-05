#!/usr/bin/env bash

set -ex

# Read ENVIRONMENT from the environment variable, default to an empty string if not set
ENVIRONMENT=${ENVIRONMENT:-}

DEFAULT_MODULE_NAME=app.app
MODULE_NAME=${MODULE_NAME:-$DEFAULT_MODULE_NAME}
VARIABLE_NAME=${VARIABLE_NAME:-app}
export APP_MODULE=${APP_MODULE:-"$MODULE_NAME:$VARIABLE_NAME"}

HOST=${HOST:-0.0.0.0}
PORT=${PORT:-8000}
LOG_LEVEL=${LOG_LEVEL:-info}
LOG_CONFIG=${LOG_CONFIG:-/finefind/logging.ini}

# Start Uvicorn with live reload if ENVIRONMENT is LOCAL

if [ "$ENVIRONMENT" = "LOCAL" ]; then
    exec python3 -m debugpy --listen 0.0.0.0:5678 -m uvicorn "$APP_MODULE" --reload --host $HOST --port $PORT --log-level $LOG_LEVEL --log-config $LOG_CONFIG
else
    exec uvicorn --reload --proxy-headers --host $HOST --port $PORT --log-config $LOG_CONFIG "$APP_MODULE"
fi
