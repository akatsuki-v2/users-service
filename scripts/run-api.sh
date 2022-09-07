#!/usr/bin/env bash
set -euo pipefail

if [ -z "$APP_ENV" ]; then
  echo "Please set APP_ENV"
  exit 1
fi

if [ "$APP_ENV" == "local" ]; then
  EXTRA_PARAMS="--reload"
else
  EXTRA_PARAMS=""
fi

exec uvicorn \
    --host 0.0.0.0 \
    --port 80 \
    --no-access-log \
    $EXTRA_PARAMS \
    app.api_boot:api
