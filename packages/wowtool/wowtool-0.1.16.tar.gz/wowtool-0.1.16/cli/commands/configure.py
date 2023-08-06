import click
import json
import os
from pathlib import Path
from cli.utils import exception_handler, config_file_exist, wowza_auth

PROFILE_HELP = """
`wowtool` profile, can be set with WOWTOOL_PROFILE env var.
profile settings in ~/.wow/config.json
"""


@click.group(invoke_without_command=True)
def configure():
    """
    Setup credentials file.
    """

    if config_file_exist():
        if click.confirm('Credentials file already exist, override?'):
            wowza_auth()
            click.echo('Credentials file successfully created!')
    else: 
        wowza_auth()
        click.echo('Credentials file successfully created!')
