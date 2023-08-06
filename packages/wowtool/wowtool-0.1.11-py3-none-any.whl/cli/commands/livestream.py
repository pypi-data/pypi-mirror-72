import json
import sys
import click
from tinydb import TinyDB, Query
from click_option_group import optgroup, RequiredMutuallyExclusiveOptionGroup
from cli.utils import exception_handler, wowza_auth, get_config_path, database_file_exist, get_database_file_path
from wowpy.livestreams import LiveStream

PROFILE_HELP = """
`wowtool` profile, can be set with WOWTOOL_PROFILE env var.
profile settings in ~/.wow/config.json
"""


@click.group()
def live():
    """
    Live Stream commands.
    """
    pass


@live.command(name='query')
@optgroup.group('Live stream identifier', cls=RequiredMutuallyExclusiveOptionGroup,
                help='Identifier for wowza live stream')
@optgroup.option('--id', help='Live stream id')
@optgroup.option('--name', help='Live stream name')
@exception_handler
def query(id, name):
    """Get data for a Live Stream"""
    wowza_auth()
    config_path = get_config_path()
    if name:
        if database_file_exist(config_path):
            config_path = get_config_path()
            database_file_path = get_database_file_path(config_path)
            ###
            db = TinyDB(database_file_path)
            query = Query()
            table = db.table('live_streams')
            response = table.search(query.live_stream_name == name)
            id = response[0]['live_stream_id']
            ###
        else:
            click.echo('In order to use --name parameter you must execute map command first')
            sys.exit()
    response = LiveStream.get_live_stream(id)
    click.echo(json.dumps(response, indent=4))

@live.command(name='start')
@optgroup.group('Live stream identifier', cls=RequiredMutuallyExclusiveOptionGroup,
                help='Identifier for wowza live stream')
@optgroup.option('--id', help='Live stream id')
@optgroup.option('--name', help='Live stream name')
@exception_handler
def start(id, name):
    """Start a Live Stream"""
    wowza_auth()
    LiveStream.start_live_stream(id)
    click.echo('Live Stream started')

@live.command(name='stop')
@optgroup.group('Live stream identifier', cls=RequiredMutuallyExclusiveOptionGroup,
                help='Identifier for wowza live stream')
@optgroup.option('--id', help='Live stream id')
@optgroup.option('--name', help='Live stream name')
@exception_handler
def stop(id, name):
    """Stop a Live Stream"""
    wowza_auth()
    LiveStream.stop_live_stream(id)
    click.echo('Live Stream stopped')

@live.command(name='state')
@optgroup.group('Live stream identifier', cls=RequiredMutuallyExclusiveOptionGroup,
                help='Identifier for wowza live stream')
@optgroup.option('--id', help='Live stream id')
@optgroup.option('--name', help='Live stream name')
@exception_handler
def state(id, name):
    """Get state for a Live Stream"""
    wowza_auth()
    state = LiveStream.get_state(id)
    click.echo('Live Stream state is {0}'.format(state))
