import discord
from log import log_commands
from cfn_api import cfn_api


def paginate(dump, max_per_page=2000):
    paginated = []
    if len(dump) < max_per_page:
        paginated.append(dump)
    else:
        page_index = 0
        len_count = 0
        split = dump.splitlines(True)
        for i, line in enumerate(split):
            if i == len(split) - 1:
                paginated.append(dump[page_index:])
            elif len_count + len(line) >= max_per_page:
                paginated.append(dump[page_index:page_index + len_count])
                page_index += len_count
                len_count = len(line)
            else:
                len_count += len(line)
    return paginated


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
        names = []
        for s in client.servers:
            names.append(f'**{s.name}** - *{s.owner.name}*')
        embed = discord.Embed(colour=0x0000ff, title=f'{len(client.servers)} servers')
        await client.send_message(message.channel, embed=embed)
        for page in paginate('\n'.join(names)):
            await client.send_message(message.channel, page)

    else:
        log_commands.info('Unknown command [%s]', message.content)
