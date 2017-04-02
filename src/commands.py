import discord
from log import log_commands
from cfn_api import cfn_api


log_commands.info(discord.__version__)


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

    elif message.content == 'test':
        embed = discord.Embed(colour=discord.Colour(0xc43f05), description="More PC Beta test servers are open to play.  Thank you for participating in this beta test.")
        embed.set_author(name="SFVServer", url="https://twitter.com/SFVServer", icon_url="https://pbs.twimg.com/profile_images/664136923309436928/AyadcsH1.png")
        embed.set_footer(text="[footer text](https://twitter.com/SFVServer/status/847962241114660864)")
        await client.send_message(message.channel, embed=embed)

    elif message.content == 'stats':
        await client.send_message(message.channel, f'{len(client.servers)} servers')

    else:
        log_commands.info('Unknown command [%s]', message.content)
