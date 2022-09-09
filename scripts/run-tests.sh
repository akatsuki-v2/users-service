#!/usr/bin/env bash
set -eo pipefail

FULL_TEST_DB_NAME="${WRITE_DB_NAME}_test"

echo "Recreating database.."
echo "Dropping database ${FULL_TEST_DB_NAME}.."
echo "DROP DATABASE IF EXISTS ${FULL_TEST_DB_NAME}" | PGPASSWORD=$WRITE_DB_PASS psql \
    --username=$WRITE_DB_USER \
    --host=$WRITE_DB_HOST \
    --dbname=postgres
echo "Creating database ${FULL_TEST_DB_NAME}"
echo "CREATE DATABASE ${FULL_TEST_DB_NAME}" | PGPASSWORD=$WRITE_DB_PASS psql \
    --username=$WRITE_DB_USER \
    --host=$WRITE_DB_HOST \
    --dbname=postgres

export WRITE_DB_NAME=$FULL_TEST_DB_NAME

echo "Running database migrations.."
/scripts/migrate-db.sh up

echo "Running database seeds.."
/scripts/seed-db.sh up

# don't generate .pyc files
export PYTHONDONTWRITEBYTECODE=1
export PYTHONPATH=$PYTHONPATH:/srv/root

cd /srv/root

pytest \
    --cov=app \
    --cov-report=term \
    tests/
