import asyncio
import discord
from config import app_config
from twitter_update import refresh_twitter_updates
import log


logging.info('app_start')


client = discord.Client()


@client.event
async def on_ready():
    logging.info('on_ready')
    client.loop.create_task(refresh_twitter_updates(client, 10 * 60))  # every 10 min


@client.event
async def on_server_join(server):
    logging.info('on_server_join \'%s\' (%s) owned by \'%s\'' % (server.name, server.id, server.owner.name))


client.run(app_config['discord_token'])
