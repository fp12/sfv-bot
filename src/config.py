import os

app_config = {}

if os.getenv('heroku') is not None:
    for k in ['heroku', 'discord_token', 'twitter_consumer_key', 'twitter_consumer_secret', 'twitter_access_token_key', 'twitter_access_token_secret', 'database', 'cookie']:
        app_config[k] = os.getenv(k)
else:
    import json
    with open('../config/config.json') as data_file:
        app_config = json.load(data_file)
