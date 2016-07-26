import asyncio
import discord
from log import log_commands
from cfn_api import cfn_api
from cfn_models import *


async def try_execute(client, message):
    if message.content == 'connect':
        log_commands.info('executing [connect] command')
        connected = await cfn_api.connect()
        if connected:
            await client.send_message(message.channel, 'CFN API CONNECTED!')
        else:
            await client.send_message(message.channel, 'Something went wrong, please check logs')

    elif message.content == 'info':
        log_commands.info('executing [info] command')
        player = await cfn_api.find_player_by_name('Backdash_Luffy')
        if player:
            await client.send_message(message.channel, 'Found Player %s - %s' % (player.name, player.cfn_id))
        else:
            await client.send_message(message.channel, 'Something went wrong, please check logs')

    else:
        log_commands.info('Unknown command [%s]', message.content)
