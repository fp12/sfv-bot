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


servers_up_txt = 'servers UP'
servers_down_txt = 'servers DOWN'


def get_server_availability(text):
    if 'beta' in text or 'Beta' in text:
        return ServerAvailability.Unknown
    if r_up.match(text):
        return ServerAvailability.Up
    if r_down.match(text):
        return ServerAvailability.Down
    return ServerAvailability.Unknown


def get_colour_for_availability(avail):
    if avail == ServerAvailability.Up:
        return discord.Colour.green()
    if avail == ServerAvailability.Down:
        return discord.Colour.red()
    return discord.Colour.dark_blue()


async def _process_new_status(client, server_status):
    log_twitter.info('Processing tweet #%s [%s]', server_status.id, server_status.text)
    db.set_last_tweet(server_status.id)
    server_availability = get_server_availability(server_status.text)

    for s in client.servers:
        bot_status = s.me.status
        old_game_name = s.me.game.name if s.me.game else ''
        break

    new_status = bot_status
    if bot_status == discord.Status.do_not_disturb:
        if server_availability == ServerAvailability.Up:
            new_status = discord.Status.online
            new_game_name = servers_up_txt
        else:
            new_game_name = servers_down_txt
    else:
        if server_availability == ServerAvailability.Down:
            new_status = discord.Status.do_not_disturb
            new_game_name = servers_down_txt
        else:
            new_game_name = servers_up_txt

    if old_game_name != new_game_name or bot_status != new_status:
        db.set_last_idle(new_status == discord.Status.do_not_disturb)
        await client.change_presence(game=discord.Game(name=new_game_name), status=new_status)
        log_twitter.info('Updated game name from [%s] to [%s] and status from [%s] to [%s]' % (old_game_name, new_game_name, bot_status, new_status))

    # send message to all registered channels
    for c in db.get_update_channels():
        channel = client.get_channel(c.channel_id)
        if channel:
            # send message
            embed = discord.Embed(colour=get_colour_for_availability(server_availability),
                                  title='New update:',
                                  url=f'https://twitter.com/{server_status.user.screen_name}/status/{server_status.id}',
                                  description=server_status.text)
            embed.set_author(name=server_status.user.name, url=server_status.user.url, icon_url=server_status.user.profile_image_url)
            try:
                new_msg = await client.send_message(channel, embed=embed)
            except Exception as e:
                log_twitter.exception(f'Exception while trying to send message on server {channel.server.name}: {e}')
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
        new_status = discord.Status.do_not_disturb
    else:
        new_game_name = servers_up_txt
        new_status = discord.Status.online
    await client.change_presence(game=discord.Game(name=new_game_name), status=new_status)
    log_twitter.info('(from last session) Updated game name to [%s] and status to [%s]' % (new_game_name, new_status))

    # main loop
    while True:
        await _do_refresh(client)
        await asyncio.sleep(interval)
