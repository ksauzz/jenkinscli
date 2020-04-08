import click
import sys

from jenkinscli import server
from jenkinscli import console


@click.group()
def plugin():
    """Plugin Commands"""
    pass


@plugin.command()
@click.option('-d', '--depth', default=4, type=int)
def list(depth):
    """List Plugins"""
    console.print_plugins(server().get_plugins(depth=depth))
