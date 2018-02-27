#!/bin/bash
docker-compose up -d
python wpc_website/manage.py runserver
