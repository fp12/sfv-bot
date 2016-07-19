import logging
from config import app_config


if 'heroku' in app_config:
    logging_level = logging.INFO
else:
    logging_level = logging.DEBUG


logging.basicConfig(format='[%(levelname)s] [%(name)s] %(message)s', level=logging_level)
