#!/bin/bash

set -e

echo "Waiting for PostgreSQL to be ready..."

while ! nc -z $DB_HOST $DB_PORT; do
  sleep 0.1
done

echo "PostgreSQL is up - applying migrations and starting application"

echo "Applying custom migrations..."
python add_remaining_amount_migration.py
python update_remaining_amount.py

echo "Starting FastAPI application..."
python run.py