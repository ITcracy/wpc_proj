import base64
import os
import uuid

from fabric.api import cd, env, lcd, local, run
from fabric.contrib.files import append, exists

REPO_URL = 'https://github.com/Codennovation/wpc_proj.git'


def h_run(*args, **kwargs):
    if env.host in ('localhost', '127.0.0.1'):
        return local(*args, **kwargs)
    else:
        return run(*args, **kwargs)


def h_exists(*args, **kwargs):
    if env.host in ('localhost', '127.0.0.1'):
        return os.path.exists(*args, **kwargs)
    else:
        return exists(*args, **kwargs)


def h_append(*args, **kwargs):
    if env.host in ('localhost', '127.0.0.1'):
        if not os.path.exists('.env'):
            local('touch .env')
        contents = local('cat {}'.format(args[0]))
        if not args[1] in contents:
            local('echo {} >> {}'.format(args[1], args[0]))
    else:
        append(*args, **kwargs)


def deploy():
    site_folder = f'/home/{env.user}/Projects/{env.host}'
    h_run(f'mkdir -p {site_folder}')
    if env.host in ('localhost', '127.0.0.1'):
        os.chdir(site_folder)
        with lcd(site_folder):
            _all_process()
    else:
        with cd(site_folder):
            _all_process()


def _all_process():
    _get_latest_source()
    _update_virtualenv()
    _create_or_update_dotenv()
    _run_docker_compose()
    _update_static_files()
    _update_database()


def _get_latest_source():
    if h_exists('.git'):
        h_run('git reset --hard')
        h_run('git pull origin master')
    else:
        h_run(f'git clone {REPO_URL} .')


def _update_virtualenv():
    h_run('pipenv install')


def _create_or_update_dotenv():
    if env.host in ('localhost', '127.0.0.1'):
        h_append('.env', 'DEBUG=True')
    else:
        h_append('.env', 'DEBUG=False')
    h_append('.env', f'ALLOWED_HOSTS={env.host}')
    h_append('.env', f'DB_USER={env.user}')
    db_pass = uuid.uuid4().hex
    h_append('.env', f'DB_PASSWORD={db_pass}')
    h_append('.env', f'DB_NAME=wpc_db')
    DATABASE_URL = f'psql://{env.user}:{db_pass}@127.0.0.1:5432/wpc_db'
    h_append('.env', f'DATABASE_URL={DATABASE_URL}')
    current_contents = h_run('cat .env')
    if 'SECRET_KEY' not in current_contents:
        new_secret = base64.b64encode(os.urandom(256))
        h_append('.env', f'SECRET_KEY={new_secret}')


def _run_docker_compose():
    h_run('pipenv run docker-compose up -d')


def _update_static_files():
    h_run('pipenv run python wpc_website/manage.py collectstatic --noinput')


def _update_database():
    h_run('pipenv run python wpc_website/manage.py migrate --noinput')
