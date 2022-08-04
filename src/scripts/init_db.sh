#!/bin/bash
export $(grep -v '^#' ../.env | xargs)

SUPERUSER_USERNAME=admin
SUPERUSER_EMAIL=admin@gmail.com
SUPERUSER_PASSWORD=admin

source ../venv/bin/activate
python manage.py makemigrations
python manage.py migrate


if [[ "$ENVIRONMENT" == 'dev' ]]; then

python manage.py runscript seeders.users.load_user
python manage.py shell -c "from accounts.models import User; super_user = User.objects.create_superuser('$SUPERUSER_USERNAME', '$SUPERUSER_EMAIL', '$SUPERUSER_PASSWORD');"

fi;