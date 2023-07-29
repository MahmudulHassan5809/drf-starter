#!/bin/sh

# Custom script to wait for PostgreSQL to be available
wait_for_postgres() {
    echo "Waiting for PostgreSQL..."
    until pg_isready -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME > /dev/null 2>&1; do
        sleep 1
    done
    echo "PostgreSQL is available."
}

# Call the function to wait for PostgreSQL
if [ "$DATABASE" = "postgres" ]; then
    wait_for_postgres
fi

# python manage.py flush --no-input
# python manage.py migrate

python manage.py collectstatic --noinput

exec "$@"
