import logging
from config import app_config


if 'heroku' in app_config:
	logging_level = logging.INFO
else:
	logging_level = logging.DEBUG


logging.basicConfig(format='[%(asctime)s] [%(levelname)s] %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging_level)
