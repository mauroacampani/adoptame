#!/bin/sh

echo "Esperando a PostgreSQL..."

while ! nc -z $DB_HOST $DB_PORT; do
  sleep 0.5
done

echo "PostgreSQL está listo"

exec "$@"
