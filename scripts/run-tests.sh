#!/usr/bin/env bash
set -eo pipefail

FULL_TEST_DB_NAME="${WRITE_DB_NAME}_test"
echo -e "\x1b[;93mRunning tests on '${FULL_TEST_DB_NAME}' database\x1b[m"

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
export READ_DB_NAME=$FULL_TEST_DB_NAME

echo "Running database migrations.."
/scripts/migrate-db.sh up

echo "Running database seeds.."
/scripts/seed-db.sh up

# make sure we're not running cache
find . -name "*.pyc" -delete
export PYTHONDONTWRITEBYTECODE=1

# use /srv/root as home
export PYTHONPATH=$PYTHONPATH:/srv/root
cd /srv/root

exec pytest tests/ \
    --cov-config=tests/coverage.ini \
    --cov=app \
    --cov-report=term \
    --cov-report=html:tests/htmlcov \
    --pdb -vv
