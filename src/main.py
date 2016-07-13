import discord
from config import app_config

client = discord.Client()
client.run(app_config['discord_token'])
