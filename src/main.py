import asyncio
import discord
from config import app_config
from twitter_update import refresh_twitter_updates
import logging
import log
from commands import try_execute


logger = logging.getLogger('Main')


logger.info('app_start')


client = discord.Client()


@client.event
async def on_ready():
    logger.info('on_ready')
    client.loop.create_task(refresh_twitter_updates(client, 2 * 60))  # every 2 min


@client.event
async def on_server_join(server):
    logger.info('on_server_join \'%s\' (%s) owned by \'%s\'' % (server.name, server.id, server.owner.name))


@client.event
async def on_server_remove(server):
    logger.info('on_server_remove \'%s\' (%s) owned by \'%s\'' % (server.name, server.id, server.owner.name))


@client.event
async def on_message(message):
    if message.author == client.user or not message.channel.is_private or message.author.id != '150316380992962562':
        return
    await try_execute(client, message)


client.run(app_config['discord_token'])
