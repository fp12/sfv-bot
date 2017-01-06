import asyncio
import re
from enum import Enum
import twitter
import discord
from config import app_config
from db_access import db
from log import log_twitter


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

servers_up_txt = 'servers UP'
servers_down_txt = 'servers DOWN'


def get_server_availability(text):
    if r_up.match(text):
        return ServerAvailability.Up
    elif r_down.match(text):
        return ServerAvailability.Down
    else:
        return ServerAvailability.Unknown


async def _process_new_status(client, server_status):
    log_twitter.info('Processing tweet #%s [%s]', server_status.id, server_status.text)
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
            new_game_name = servers_up_txt
        else:
            new_game_name = servers_down_txt
    else:
        if server_availability == ServerAvailability.Down:
            new_idle = True
            new_game_name = servers_down_txt
        else:
            new_game_name = servers_up_txt

    if old_game_name != new_game_name or old_idle != new_idle:
        db.set_last_idle(new_idle)
        await client.change_status(game=discord.Game(name=new_game_name), idle=new_idle)
        log_twitter.info('Updated game name from [%s] to [%s] and idle from [%s] to [%s]' % (old_game_name, new_game_name, old_idle, new_idle))

    # send message to all registered channels
    for c in db.get_update_channels():
        channel = client.get_channel(c.channel_id)
        if channel:
            # send message
            new_msg = await client.send_message(channel, update_template % server_status.text)

            if server_availability != ServerAvailability.Unknown:
                # unpin last message
                try:
                    old_msg = await client.get_message(channel, c.last_message)
                    await client.unpin_message(old_msg)
                except Exception as e:
                    log_twitter.exception('Exception while trying to unpin message on server %s: %s' % (c.server_id, e))

                # pin new message
                try:
                    await client.pin_message(new_msg)
                except Exception as e:
                    log_twitter.exception('Exception while trying to pin message on server %s: %s' % (c.server_id, e))

            # store last message
            db.set_last_message(c.channel_id, new_msg.id)
        else:
            log_twitter.error('Channel not set for server %s' % c.server_id)


async def _do_refresh(client):
    last_id = db.get_last_tweet().value
    server_statuses = api.GetHomeTimeline(exclude_replies=True, since_id=last_id)
    server_statuses.sort(key=lambda status: status.id)
    log_twitter.info('_do_refresh with %s new status' % len(server_statuses))
    for s in server_statuses:
        await _process_new_status(client, s)


async def refresh_twitter_updates(client, interval):
    # recover from last session
    was_idle = db.get_last_idle().value == 'True'
    if was_idle:
        new_game_name = servers_down_txt
    else:
        new_game_name = servers_up_txt
    await client.change_status(game=discord.Game(name=new_game_name), idle=was_idle)
    log_twitter.info('(from last session) Updated game name to [%s] and idle to [%s]' % (new_game_name, was_idle))

    # main loop
    while True:
        await _do_refresh(client)
        await asyncio.sleep(interval)
