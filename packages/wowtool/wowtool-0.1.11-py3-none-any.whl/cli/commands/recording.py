import json
import click
from click_option_group import optgroup, RequiredMutuallyExclusiveOptionGroup
from wowpy.recordings import Recording
from cli.utils import exception_handler, wowza_auth

PROFILE_HELP = """
`wowtool` profile, can be set with WOWTOOL_PROFILE env var.
profile settings in ~/.wow/config.json
"""

@click.group()
def recording():
    """
    Recording commands.
    """
    pass


@recording.command(name='query')
@optgroup.group('Recording identifier', cls=RequiredMutuallyExclusiveOptionGroup,
                help='Identifier for wowza recording')
@optgroup.option('--id', help='Transcoder id')
@optgroup.option('--name', help='Transcoder name')
@exception_handler
def query(id, name):
    """Get Recording"""
    wowza_auth()
    response = Recording.get_recording(id)
    click.echo(json.dumps(response, indent=4))