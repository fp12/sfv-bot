import asyncio
import discord
from config import app_config
from twitter_update import refresh_twitter_updates


print('app_start')


client = discord.Client()


@client.event
async def on_ready():
    print('on_ready')
    client.loop.create_task(refresh_twitter_updates(client, 10 * 60))  # every 10 min


client.run(app_config['discord_token'])
