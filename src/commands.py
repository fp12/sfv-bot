import asyncio
import discord
import logging
import log
from cfn_api import cfn_api
from cfn_models import *


async def try_execute(client, message):
    if message.content == 'connect':
        logging.info('executing [connect] command')
        connected = await cfn_api.connect()
        if connected:
            client.send_message(message.channel, 'CFN API CONNECTED!')
        else:
            client.send_message(message.channel, 'Something went wrong, please check logs')

    elif message.content == 'info':
        logging.info('executing [info] command')
        player = await cfn_api.find_player_by_name('Backdash_Luffy')
        if player:
            client.send_message(message.channel, 'Found Player %s - %s' % (player.name, player.cfn_id))
        else:
            client.send_message(message.channel, 'Something went wrong, please check logs')
            
    else:
        logging.info('Unknown command [%s]', message.content)
