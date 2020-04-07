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
    if config.insecure:
        # this is defined in jenkins
        os.environ['PYTHONHTTPSVERIFY'] = '0'

    def mask(secret):
        if not secret:
            return secret
        elif len(secret) < 4:
            return '*' * len(secret)
        else:
            return secret[:3] + '*' * (len(secret) - 3)

    format = "{:10}: {}"
    logger.debug(format.format('url', config.url))
    logger.debug(format.format('name', config.user))
    logger.debug(format.format('password', mask(config.password)))
    logger.debug(format.format('insecure', config.insecure))


main.add_command(job)
main.add_command(build)
main.add_command(validate)
