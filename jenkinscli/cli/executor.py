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
            elif node['offline']:
                displayname = 'offline'
            else:
                displayname = 'idle'
            executor_name = "{} ({})".format(node['name'], executor['number']+1)
            click.echo('{:15} {}'.format(executor_name, displayname))
