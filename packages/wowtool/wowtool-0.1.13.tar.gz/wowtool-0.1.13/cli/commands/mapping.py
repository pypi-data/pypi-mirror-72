import json
import click
from tinydb import TinyDB
from click_option_group import optgroup, RequiredMutuallyExclusiveOptionGroup
from cli.utils import exception_handler, wowza_auth, get_config_path, get_database_file_path
from wowpy.mappings import Mapper

PROFILE_HELP = """
`wowtool` profile, can be set with WOWTOOL_PROFILE env var.
profile settings in ~/.wow/config.json
"""

@click.group()
def mapper():
    """
    Mapping commands.
    """
    pass


@mapper.command(name='live_streams')
@exception_handler
def live_streams():
    """Map live stream ids with resource names"""
    wowza_auth()
    document_batch = Mapper.map_live_streams()
    config_path = get_config_path()
    database_file_path = get_database_file_path(config_path)
    ###
    db = TinyDB(database_file_path)
    table = db.table('live_streams')
    table.insert_multiple(document_batch)
    ###
    click.echo('Mapping of live stream ids with resource names done')

@mapper.command(name='recordings')
@exception_handler
def recordings():
    """Map recording ids with resource names"""
    wowza_auth()
    document_batch = Mapper.map_recordings()
    config_path = get_config_path()
    database_file_path = get_database_file_path(config_path)
    ###
    db = TinyDB(database_file_path)
    table = db.table('recordings')
    table.insert_multiple(document_batch)
    ###
    click.echo('Mapping of recording ids with resource names done')

# TODO: Create a map all, taking into account some resources like targets and recordings will be null