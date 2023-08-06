import json
import click
from click_option_group import optgroup, RequiredMutuallyExclusiveOptionGroup
from cli.utils import exception_handler, wowza_auth
from wowpy.resources import get_resource_info
from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import TerminalTrueColorFormatter

PROFILE_HELP = """
`wowtool` profile, can be set with WOWTOOL_PROFILE env var.
profile settings in ~/.wow/config.json
"""


@click.group()
def resource():
    """
    Resource commands.
    """
    pass


@resource.command(name='query')
@optgroup.group('Resource identifier', cls=RequiredMutuallyExclusiveOptionGroup,
                help='Identifier for resource')
@optgroup.option('--id', help='Resource id')
@optgroup.option('--name', help='Resource name')
@exception_handler
def query(id, name):
    """Get data for resource"""
    wowza_auth()
    response = get_resource_info(id)
    formatted_json = json.dumps(response, indent=4)
    colorful_json = highlight(formatted_json, JsonLexer(), TerminalTrueColorFormatter(style='solarized-dark'))
    click.echo(colorful_json)
