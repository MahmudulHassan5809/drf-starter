#!/bin/bash
export $(grep -v '^#' ../.env | xargs)
DB_NAME=$DB_NAME
DB_USER=$DB_USER
DB_PASSWORD=$DB_PASSWORD
sudo su postgres <<EOF
psql -c "DROP DATABASE $DB_NAME;"
psql -c "CREATE DATABASE $DB_NAME;"
psql -c "grant all privileges on database $DB_NAME to $DB_USER;"
echo "Postgres User '$DB_USER' and database '$DB_NAME' created."
EOF