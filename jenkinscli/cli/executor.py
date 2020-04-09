import click
import sys

from jenkinscli import server
from jenkinscli import console


@click.group()
def executor():
    """Executor Commands"""
    pass


@executor.command()
def list():
    """List Executor"""
    for node in server().get_nodes(depth=2):
        node_name = '(master)' if node['name'] == 'master' else node['name']
        node_info = server().get_node_info(node_name, depth=2)
        for executor in sorted(node_info['executors'], key=lambda x: x['number']):
            displayname = executor.get('currentExecutable')
            if displayname:
                displayname = displayname.get('displayName')
            else:
                displayname = 'idle'
            status = 'online' if not node['offline'] else 'offline'
            click.echo('{:10} {} {:7} {}'.format(node['name'], executor['number'], status, displayname))
