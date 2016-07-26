import logging
from config import app_config


if 'heroku' in app_config:
    logging_level = logging.INFO
else:
    logging_level = logging.DEBUG


logging.basicConfig(format='[%(levelname)s] [%(name)s] %(message)s', level=logging_level)

log_main = logging.getLogger('Main')
log_twitter = logging.getLogger('Twitter')
log_db = logging.getLogger('DB')
log_commands = logging.getLogger('Commands')
log_cfn = logging.getLogger('CFN')
