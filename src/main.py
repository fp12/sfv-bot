import discord
from config import app_config
from twitter_update import refresh_twitter_updates
from log import log_main
from commands import try_execute


log_main.info('app_start')
log_main.info(discord.__version__)


client = discord.Client()


@client.event
async def on_ready():
    log_main.info('on_ready')
    client.loop.create_task(refresh_twitter_updates(client, 2 * 60))  # every 2 min


@client.event
async def on_server_join(server):
    log_main.info('on_server_join \'%s\' (%s) owned by \'%s\'' % (server.name, server.id, server.owner.name))


@client.event
async def on_server_remove(server):
    log_main.info('on_server_remove \'%s\' (%s) owned by \'%s\'' % (server.name, server.id, server.owner.name))


@client.event
async def on_message(message):
    if message.author == client.user or not message.channel.is_private or message.author.id != '150316380992962562':
        return
    await try_execute(client, message)


client.run(app_config['discord_token'])
