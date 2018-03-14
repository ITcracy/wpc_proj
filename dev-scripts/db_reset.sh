#!/bin/bash
echo "Stopping and Deleting containers"
pipenv run docker-compose rm -fs

echo "Creating new containers"
pipenv run docker-compose up -d

echo "Waiting for 15 seconds"
sleep 15

echo "Deleting migrations"
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete

echo "Making migrations"
pipenv run wpc_website/manage.py makemigrations

echo "Migrating"
pipenv run wpc_website/manage.py migrate

echo "Creating superuser"
echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'nimda')" | pipenv run python wpc_website/manage.py shell
