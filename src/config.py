import os

app_config = []

if os.getenv('heroku') is not None:
    for k in ['discord_token']:
        app_config[k] = os.getenv(k)
else:
    import json
    with open('../config/config.json') as data_file:
        app_config = json.load(data_file)
