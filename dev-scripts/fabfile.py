import base64
import os
import uuid

from fabric.api import cd, env, lcd, local, put, run, settings, sudo
from fabric.contrib.files import append, exists, upload_template

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


def _prerequisites():
    if env.host not in ('localhost', '127.0.0.1'):
        with settings(warn_only=True):
            nginx = run("nginx -v")
        if nginx.failed:
            sudo("apt-get install python3-pip python3-dev nginx git")
            sudo("pip3 install pipenv")
            return True
        else:
            return False


def install_docker():
    """
    Installs docker on the remote server and adds docker to sudoers group.
    Should be called separately from deploy for the first time.
    """
    sudo("apt-get update")
    sudo("apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    software-properties-common")
    run("curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -"
        )
    command = 'add-apt-repository \
    "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
    $(lsb_release -cs) \
    stable"'

    sudo(command)
    sudo("apt-get update")
    sudo("apt-get install docker-ce")
    sudo("groupadd docker")
    sudo("usermod -aG docker $USER")


def _upload_installation_files():
    gunicorn_data = {"username": env.user, "venv_path": run("pipenv --venv")}
    upload_template(
        "gunicorn.service",
        "/etc/systemd/system/gunicorn.service",
        context=gunicorn_data,
        template_dir=".",
        use_sudo=True)
    nginx_data = {"hostname": env.host, "username": env.user}
    upload_template(
        "wpc_proj",
        "/etc/nginx/sites-available/wpc_proj",
        context=nginx_data,
        template_dir=".",
        use_sudo=True)


def _file_commands():
    sudo("systemctl start gunicorn")
    sudo("systemctl enable gunicorn")
    sudo("ln -s /etc/nginx/sites-available/wpc_proj /etc/nginx/sites-enabled")
    sudo("systemctl restart nginx")
    sudo("ufw allow 'Nginx Full'")


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
    site_folder = f'/home/{env.user}/wpc/wpc_proj'
    h_run(f'mkdir -p {site_folder}')
    if env.host in ('localhost', '127.0.0.1'):
        site_folder = '../'
        with lcd(site_folder):
            _all_process()
    else:
        with cd(site_folder):
            _all_process()


def _all_process():
    new = _prerequisites()
    _get_latest_source()
    _update_virtualenv()
    if env.host in ('localhost', '127.0.0.1'):
        _create_or_update_dotenv()
    else:
        _copy_env_file()
    _run_docker_compose()
    _update_static_files()
    _update_database()
    if new:
        _upload_installation_files()
        _file_commands()
    else:
        sudo("systemctl restart gunicorn")


def _get_latest_source():
    if h_exists('.git'):
        h_run('git reset --hard')
        h_run('git pull origin master')
    else:
        h_run(f'git clone {REPO_URL} .')


def _update_virtualenv():
    h_run('pipenv install --skip-lock')


def _copy_env_file():
    if not h_exists('.env'):
        put('../.env', '.env')
        append('.env', 'DEBUG=False')
        append('.env', f'ALLOWED_HOSTS={env.host}')


def _create_or_update_dotenv():
    if env.host in ('localhost', '127.0.0.1'):
        h_append('.env', 'DEBUG=True')
    else:
        h_append('.env', 'DEBUG=False')
    h_append('.env', f'ALLOWED_HOSTS={env.host}')
    h_append('.env', f'DB_USER={env.user}')
    h_append('.env', f'DB_NAME=wpc_db')
    current_contents = h_run('cat .env')
    if 'DB_PASSWORD' not in current_contents:
        db_pass = uuid.uuid4().hex
        h_append('.env', f'DB_PASSWORD={db_pass}')
        DATABASE_URL = f'psql://{env.user}:{db_pass}@127.0.0.1:5432/wpc_db'
        h_append('.env', f'DATABASE_URL={DATABASE_URL}')
    if 'SECRET_KEY' not in current_contents:
        new_secret = base64.b64encode(os.urandom(256))
        h_append('.env', f'SECRET_KEY={new_secret}')


def _run_docker_compose():
    h_run('pipenv run docker-compose up -d')


def _update_static_files():
    h_run('pipenv run python wpc_website/manage.py collectstatic --noinput')


def _update_database():
    h_run('pipenv run python wpc_website/manage.py migrate --noinput')
