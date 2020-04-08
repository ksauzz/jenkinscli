import click
import sys

from jenkinscli import server
from jenkinscli import console


@click.group()
def plugin():
    """Plugin Commands"""
    pass


@plugin.command()
@click.option('-d', '--depth', default=4, type=int, metavar='DEPTH')
def list(depth):
    """List Plugins"""
    console.print_plugins(server().get_plugins(depth=depth))


@plugin.command()
@click.argument('name')
def install(name):
    """Install Plugin"""
    server().install_plugin(name)
