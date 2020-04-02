import click
import jenkins
import os
import logging

from jenkinscli import config
from jenkinscli import console
from jenkinscli import server
from jenkinscli.cli.job import job
from jenkinscli.cli.build import build


logformat = '%(asctime)s %(levelname)s %(message)s'
logging.basicConfig(format=logformat, level=logging.WARN)

logger = logging.getLogger(__name__)

def set_loglevel(verbose):
    if verbose > 0:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.debug('change loglevel to DEBUG')


@click.group()
@click.option('--url')
@click.option('--user')
@click.option('--password')
@click.option('-k', '--insecure', is_flag=True)
@click.option('-v', '--verbose', count=True)
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

    import jenkinscli
    jenkinscli.connect(config.url, config.user, config.password)


main.add_command(job)
main.add_command(build)
