import click
import requests
import logging

from jenkinscli import server

logger = logging.getLogger(__name__)

@click.command()
@click.argument('jenkinsfile', type=click.File('rb'), default='Jenkinsfile')
def validate(jenkinsfile):
    """Validate Jenkinsfile"""
    logger.debug('validating {}...'.format(jenkinsfile.name))
    response = server().check_jenkinsfile_syntax(jenkinsfile.read())
    if 'error' in response:
        click.echo("Error: {}".format(response['error']))
    else:
        click.echo("Jenkinsfile successfully validated.")
