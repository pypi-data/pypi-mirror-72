import functools
import click
import datetime
import json
import os
from pathlib import Path

def exception_handler(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            message = 'There was an error in the CLI: {}'.format(str(e))
            click.echo(message, err=True)
            exit(1)

    return wrapper

def wowza_auth():
    config_path = get_config_path()
    if credentials_file_exist(config_path):
        set_credentials_envars(config_path)
    else:
        create_creds_file(config_path)
        set_credentials_envars(config_path)

def get_config_path():
    home_path = str(Path.home())
    config_path = home_path + '/.wow/'
    return config_path

def credentials_file_exist(config_path):
    credentials_file_path = get_credentials_file_path(config_path)
    if os.path.exists(credentials_file_path):
        return True
    else:
        return False

def database_file_exist(config_path):
    credentials_file_path = get_database_file_path(config_path)
    if os.path.exists(credentials_file_path):
        return True
    else:
        return False

def get_credentials_file_path(config_path):
    credentials_file_path = config_path + 'config.json'
    return credentials_file_path

def get_database_file_path(config_path):
    database_file_path = config_path + 'database.json'
    return database_file_path

def set_credentials_envars(config_path):
    credentials_file_path = get_credentials_file_path(config_path)
    with open(credentials_file_path) as json_file:
        credentials_data = json.load(json_file)
        os.environ["WSC_ACCESS_KEY"] = credentials_data['WSC_ACCESS_KEY']
        os.environ["WSC_API_KEY"] = credentials_data['WSC_API_KEY']

def create_creds_file(config_path):
    wsc_access_key = click.prompt('Please enter wowza access key')
    wsc_api_key = click.prompt('Please enter wowza api key')
    keys = {
            'WSC_ACCESS_KEY': wsc_access_key,
            'WSC_API_KEY': wsc_api_key
            }
    Path(config_path).mkdir(parents=True, exist_ok=True)
    credentials_file_path = get_credentials_file_path(config_path)
    with open(credentials_file_path, 'w') as json_file:
        json_file.write(json.dumps(keys, indent=4))