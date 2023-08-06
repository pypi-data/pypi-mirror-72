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

# core auth

def wowza_auth():
    if config_file_exist():
        __set_credentials_envars()
    else:
        __create_creds_file()
        __set_credentials_envars()

def __set_credentials_envars():
    credentials_file_path = get_base_file_path()
    with open(credentials_file_path) as json_file:
        credentials_data = json.load(json_file)
        os.environ["WSC_ACCESS_KEY"] = credentials_data['WSC_ACCESS_KEY']
        os.environ["WSC_API_KEY"] = credentials_data['WSC_API_KEY']

def __create_creds_file():
    config_path=__get_config_path()
    wsc_access_key = click.prompt('Please enter wowza access key')
    wsc_api_key = click.prompt('Please enter wowza api key')
    keys = {
            'WSC_ACCESS_KEY': wsc_access_key,
            'WSC_API_KEY': wsc_api_key
            }
    Path(config_path).mkdir(parents=True, exist_ok=True)
    credentials_file_path = get_base_file_path()
    with open(credentials_file_path, 'w') as json_file:
        json_file.write(json.dumps(keys, indent=4))

# core paths

def __get_config_path():
    home_path = str(Path.home())
    config_path = home_path + '/.wow/'
    return config_path

def __get_config_filename():
    config_filename = 'config.json'
    return config_filename

def config_file_exist(config_path=__get_config_path(), filename=__get_config_filename()):
    base_file_path = get_base_file_path(config_path, filename=filename)
    if os.path.exists(base_file_path):
        return True
    else:
        return False

def get_base_file_path(config_path=__get_config_path(), filename=__get_config_filename()):
    full_file_path = config_path + filename
    return full_file_path
