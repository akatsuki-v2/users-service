#!/usr/bin/env bash
set -euo pipefail

if [ -z "$APP_COMPONENT" ]; then
  echo "Please set APP_COMPONENT"
  exit 1
fi

cd /srv/root

# await connected service availability
/scripts/await-service.sh $READ_DB_HOST $READ_DB_PORT
/scripts/await-service.sh $WRITE_DB_HOST $WRITE_DB_PORT
# /scripts/await-service.sh $AMQP_HOST $AMQP_PORT
# /scripts/await-service.sh $ES_HOST $ES_PORT

# run sql database migrations & seeds
# /scripts/migrate-db up
# /scripts/seed-db up

# ensure es indices exist
# /scripts/es-init

case $APP_COMPONENT in
  "api")
    /scripts/run-api.sh
    ;;

  "tests")
    /scripts/run-tests.sh
    ;;

  *)
    echo "'$APP_COMPONENT' is not a known value for APP_COMPONENT"
esac
