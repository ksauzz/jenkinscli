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
    logger.debug('response: {}'.format(response))
    if len(response) == 0:
        click.echo("Jenkinsfile successfully validated.")
    else:
        for r in response:
            if 'error' in r:
                if type(r['error']) == str:
                    click.echo(r['error'])
                elif type(r['error']) == list:
                    for err in r['error']:
                        click.echo(err)
                else:
                    logger.error("unexpected response form: {}".format(r))
