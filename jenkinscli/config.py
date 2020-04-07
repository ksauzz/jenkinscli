import sys
import yaml
import os
import logging

logger = logging.getLogger(__name__)

url = None
user = None
password = None
insecure = None

GLOBAL_CONFIG_FILE = os.path.join(os.path.expanduser('~'), '.jenkinscli')
LOCAL_CONFIG_FILE = os.path.join(os.getcwd(), '.jenkinscli')


def init(url=None, user=None, password=None, insecure=None):
    this = sys.modules[__name__]

    config = _config()

    def get_or_default(config, key, default):
        return config.get(key) if key in config else default

    this.url = get_or_default(config, 'url', url)
    this.user = get_or_default(config, 'user', user)
    this.password = get_or_default(config, 'password', password)
    this.insecure = get_or_default(config, 'insecure', insecure)

    if this.insecure:
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
    logger.debug(format.format('url', this.url))
    logger.debug(format.format('name', this.user))
    logger.debug(format.format('password', mask(this.password)))
    logger.debug(format.format('insecure', this.insecure))


def _config():
    config = __config(LOCAL_CONFIG_FILE)
    return config if config else __config(GLOBAL_CONFIG_FILE)


def __config(config_file):
    if os.path.exists(config_file):
        logger.debug("{} was found. loading configurations from it...". format(config_file))
        with(open(config_file, 'r')) as f:
            return yaml.load(f.read(), Loader=yaml.FullLoader)
