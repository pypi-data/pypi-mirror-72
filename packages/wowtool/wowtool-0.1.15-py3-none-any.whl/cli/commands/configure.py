import click
import json
import os
from pathlib import Path
from cli.utils import exception_handler, create_creds_file, credentials_file_exist, get_config_path

PROFILE_HELP = """
`wowtool` profile, can be set with WOWTOOL_PROFILE env var.
profile settings in ~/.wow/config.json
"""


@click.group(invoke_without_command=True)
def configure():
    """
    Setup credentials file.
    """

    config_path = get_config_path()
    if credentials_file_exist(config_path):
        if click.confirm('Credentials file already exist, override?'):
            create_creds_file(config_path)
            click.echo('Credentials file successfully created!')
    else: 
        create_creds_file(config_path)
        click.echo('Credentials file successfully created!')
