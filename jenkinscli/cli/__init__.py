import click
import jenkins
import os
import logging

from jenkinscli import config
from jenkinscli import console
from jenkinscli import server
from jenkinscli.cli.job import job
from jenkinscli.cli.build import build
from jenkinscli.cli.validate import validate


logformat = '%(asctime)s %(levelname)s %(message)s'
logging.basicConfig(format=logformat, level=logging.WARN)

logger = logging.getLogger(__name__)


def set_loglevel(verbose):
    if verbose > 0:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.debug('change loglevel to DEBUG')


@click.group()
@click.option('--url', metavar='URL', help='jenkins\' endpoint')
@click.option('--user', metavar='USER', help='jenkins\' user')
@click.option('--password', metavar='PASSWORD', help='jenkins\' API token')
@click.option('-k', '--insecure', is_flag=True, help='disable verifying server certificate')
@click.option('-v', '--verbose', count=True, help='verbose log')
def main(**kwargs):
    set_loglevel(kwargs['verbose'])
    del kwargs['verbose']

    config.init(**kwargs)


main.add_command(job)
main.add_command(build)
main.add_command(validate)
