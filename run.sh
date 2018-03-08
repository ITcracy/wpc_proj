#!/bin/bash
pipenv run docker-compose up -d
pipenv run python wpc_website/manage.py runserver
