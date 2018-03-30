release: yes "yes" | python wpc_website/manage.py makemigrations && python wpc_website/manage.py migrate
web: gunicorn --chdir wpc_website wpc_website.wsgi
