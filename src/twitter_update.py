import asyncio
import re
from enum import Enum
import twitter
import discord
from config import app_config
from db_access import db

class ServerAvailability(Enum):
    Unknown = -1
    Up = 1
    Down = 0


api = twitter.Api(consumer_key=app_config['twitter_consumer_key'],
                  consumer_secret=app_config['twitter_consumer_secret'],
                  access_token_key=app_config['twitter_access_token_key'],
                  access_token_secret=app_config['twitter_access_token_secret'])


r_up = re.compile(r""".*servers.+are\s(.*\s)?(open|up)[,!\.\s].*""", re.IGNORECASE)
r_down = re.compile(r""".*servers.+are\s(.*\s)?(down|offline)[,!\.\s].*""", re.IGNORECASE)


update_template = """```ruby
Update From SFVServer (Twitter):
# %s
```"""

def get_server_availability(text):
    if r_up.match(text):
        return ServerAvailability.Up
    elif r_down.match(text):
        return ServerAvailability.Down
    else:
        return ServerAvailability.Unknown


async def _process_new_status(client, server_status):
    db.set_last_tweet(server_status.id)
    server_availability = get_server_availability(server_status.text)
    for s in client.servers:
        bot_status = s.me.status
        old_game_name = s.me.game.name if s.me.game else ''
        break
    new_idle = old_idle = bot_status == discord.Status.idle
    if old_idle:
        if server_availability == ServerAvailability.Up:
            new_idle = False
            new_game_name = 'servers UP'
        else:
            new_game_name = 'servers DOWN'
    else:
        if server_availability == ServerAvailability.Down:
            idle = True
            new_game_name = 'servers DOWN'
        else:
            new_game_name = 'servers UP'
    if old_game_name != new_game_name or old_idle != new_idle:
        print('updated game name from [%s] to [%s] and idle from [%s] to [%s]' % (old_game_name, new_game_name, old_idle, new_idle))
        await client.change_status(game=discord.Game(name=new_game_name), idle=new_idle)

    # send message to all registered channels
    for c in db.get_update_channels():
        await client.send_message(discord.Channel(id=c.channel_id), update_template % server_status.text)


async def _do_refresh(client):
    last_id = db.get_last_tweet().value
    server_statuses = api.GetHomeTimeline(exclude_replies=True, since_id=last_id)
    for s in server_statuses:
        await _process_new_status(client, s)


async def refresh_twitter_updates(client, interval):
    while True:
        await _do_refresh(client)
        await asyncio.sleep(interval)
