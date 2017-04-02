import discord
from log import log_commands
from cfn_api import cfn_api
import twitter
from db_access import db
from config import app_config


api = twitter.Api(consumer_key=app_config['twitter_consumer_key'],
                  consumer_secret=app_config['twitter_consumer_secret'],
                  access_token_key=app_config['twitter_access_token_key'],
                  access_token_secret=app_config['twitter_access_token_secret'])


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
        last_id = db.get_last_tweet().value
        server_status = api.GetHomeTimeline(exclude_replies=True, since_id=last_id)[0]
        col = discord.Colour(0x5961870) if new_status == discord.Status.online else discord.Colour.dark_magenta()
        embed = discord.Embed(colour=col, title=f'[New update](https://twitter.com/{server_status.user.screen_name}/status/{server_status.id})', description=server_status.text)
        embed.set_author(name=server_status.user.name, url=server_status.user.url, icon_url=server_status.user.profile_image_url)
        await client.send_message(message.channel, embed=embed)

    elif message.content == 'stats':
        names = []
        for s in client.servers:
            names.append(f'**{s.name}** ({s.id}) - *{s.owner.name}*')
        embed = discord.Embed(colour=0x0000ff, title=f'{len(client.servers)} servers')
        await client.send_message(message.channel, embed=embed)
        for page in paginate('\n'.join(names)):
            await client.send_message(message.channel, page)

    else:
        log_commands.info('Unknown command [%s]', message.content)
