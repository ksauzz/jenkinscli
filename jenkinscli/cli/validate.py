import click
import requests

from jenkinscli import server


@click.command()
@click.argument('jenkinsfile', type=click.File('rb'), default='Jenkinsfile')
def validate(jenkinsfile):
    """Validate Jenkinsfile"""
    response = server().check_jenkinsfile_syntax(jenkinsfile.read())
    if 'error' in response:
        click.echo("Error: {}".format(response['error']))
    else:
        click.echo("Jenkinsfile successfully validated.")
