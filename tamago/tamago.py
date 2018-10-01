#!/usr/bin/env python3
"""
Tamago BOT LIVES!
"""
import asyncio
import random
import os
import json
import argparse
import discord
import logging
import coloredlogs
import youtube_dl
from . import VERSION
from discord import Game
from discord.ext import commands
from discord.ext.commands import Bot
from itertools import cycle


PLAYERS = {}
QUEUES = {}
LOG = logging.getLogger(__name__)
BOT_PREFIX = ("?", "!")
client = Bot(command_prefix=BOT_PREFIX)
client.remove_command('help')

def parse_arguments():
    """parsing arguments.

    """
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--debug', help='enable debug', action='store_true')
    parser.add_argument('--version', action='version',
                        version=format(VERSION),
                        help='show the version number and exit')
    return parser.parse_args()

async def change_status():
    status = ['God = Ginger', 'Expresso is lame!', 'Vern\'s woo']
    await client.wait_until_ready()
    sts = cycle(status)

    while not client.is_closed:
        current_status = next(sts)
        await client.change_presence(game=discord.Game(name=current_status))
        await asyncio.sleep(15)

@client.command(pass_context=True)
async def help(ctx):
    author = ctx.message.author

    embed = discord.Embed(
        colour = discord.Colour.orange()
    )

    embed.set_author(name='Help')
    embed.add_field(name='!ping', value='Returns Pong!', inline=False)
    embed.add_field(name='!8ball', value='Shakes Magic 8ball for answer', inline=False)

    await client.send_message(author, embed=embed)

@client.command(name='8ball',
                description="Answers a yes/no question.",
                brief="Answers from the beyond.",
                aliases=['eight_ball', 'eightball', '8-ball'],
                pass_context=True)
async def eight_ball(context):
    possible_responses = [
        'That is a resounding no',
        'It is not looking likely',
        'Too hard to tell',
        'It is quite possible',
        'Definitely',
    ]
    await client.say(random.choice(possible_responses) + ", " + context.message.author.mention)

@client.event
async def on_reaction_add(reaction, user):
    channel = reaction.message.channel
    await client.send_message(channel, '{} has added {} to the message: {}'.format(user.name, reaction.emoji, reaction.message.content))

@client.event
async def on_reaction_remove(reaction, user):
    channel = reaction.message.channel
    await client.send_message(channel, '{} has remmoved {} to the message: {}'.format(user.name, reaction.emoji, reaction.message.content))

@client.command(pass_context=True)
async def hello(context):
    await client.say("Hello " + context.message.author.mention)

@client.event
async def on_command_error(error, ctx):
    msg_channel = ctx.message.channel
    if isinstance(error, commands.CommandInvokeError):
        LOG.error(error)
        await client.send_message(msg_channel, '{} Error running the command'.format(ctx.message.author.mention))

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('expresso'):
        msg = 'https://scontent-sea1-1.xx.fbcdn.net/v/t1.0-9/5018_110506398392_7227641_n.jpg?_nc_cat=103&oh=09d93ddbb2a1d5f653895ba67b71845b&oe=5C5AA237'.format(message)
        await client.send_message(message.channel, msg)

    await client.process_commands(message)

@client.event
async def on_ready():
    await client.change_presence(game=Game(name="with humans"))
    LOG.info("Logged in as " + client.user.name)

@client.command()
async def bitcoin():
    url = 'https://api.coindesk.com/v1/bpi/currentprice/BTC.json'
    async with aiohttp.ClientSession() as session:  # Async HTTP request
        raw_response = await session.get(url)
        response = await raw_response.text()
        response = json.loads(response)
        await client.say("Bitcoin price is: $" + response['bpi']['USD']['rate'])

@client.command()
async def ping():
    await client.say('Pong')

async def list_servers():
    await client.wait_until_ready()
    while not client.is_closed:
        server_list = []
        for server in client.servers:
            server_list.append(server.name)
        LOG.info('Current servers: {}'.format(server_list))
        await asyncio.sleep(600)

@client.command(pass_context=True)
async def clear(ctx, amount=5):
    channel = ctx.message.channel
    messages = []

    async for message in client.logs_from(channel, limit=int(amount) + 1):
        messages.append(message)
    await client.delete_messages(messages)
    await client.say('%s messages purged' % amount)

@client.command()
async def tamago():
    embed = discord.Embed(
        title = 'Title',
        description = 'Test description',
        colour = discord.Colour.gold()
    )

    embed.set_image(url='https://pbs.twimg.com/profile_images/536300196326412288/BiNSl6fJ_400x400.png')
    embed.set_author(name='Benidct Tamago')
    embed.set_thumbnail(url='https://kikusushi.ca/dynamic_content/product_images/5/x533_50befac8f6b00a5ec710a911b675a98b.jpg.pagespeed.ic.Zsju56w-VL.webp')
    embed.add_field(name='description', value='Bot is a WIP, have fun!', inline=False)

    await client.say(embed=embed)


"""
VOICE
"""

@client.command(pass_context=True)
async def join(ctx):
    msg_channel = ctx.message.channel
    voice_channel = ctx.message.author.voice.voice_channel
    try:
        await client.join_voice_channel(voice_channel)
    except Exception as e:
        LOG.error(e)
        await client.send_message(msg_channel, '{} DERP! you are currently not in a voice channel, unable to join'.format(ctx.message.author.mention))

@client.command(pass_context=True)
async def leave(ctx):
    msg_channel = ctx.message.channel
    server  = ctx.message.author.server
    if client.is_voice_connected(server):
        voice_client = client.voice_client_in(server)
        await voice_client.disconnect()
    else:
        await client.send_message(msg_channel, '{} Tamago BOT is currently not in a voice channel, can\'t disconnect!'.format(ctx.message.author.mention))

"""
Music
"""

# @client.command(pass_context=True)
# async def play(ctx, url):
#     server = ctx.message.server
#     voice_client = client.voice_client_in(server)
#     player = await voice_client.create_ytdl_player(url, after=lambda: check_queue(server.id))
#     PLAYERS[server.id] = player
#     player.start()

@client.command(pass_context=True)
async def play(ctx, url):
    opts = {
     'default_search': 'auto',
     'quiet': False,
    }
    before_options = '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 2'
    server = ctx.message.server

    if server.id in PLAYERS:
         LOG.info("stopping current player before second player starts")
         PLAYERS[server.id].stop()

    voice_client = client.voice_client_in(server)
    player = await voice_client.create_ytdl_player(url,
                                                   ytdl_options=opts,
                                                   before_options=before_options,
                                                   after=lambda: check_queue(server.id))
    PLAYERS[server.id] = player
    player.start()


@client.command(pass_context=True)
async def pause(ctx):
    server_id = ctx.message.server.id
    PLAYERS[server_id].pause()

@client.command(pass_contex=True)
async def resume(ctx):
    server_id = ctx.message.server.id
    PLAYERS[server_id].resume()

@client.command(pass_contex=True)
async def stop(ctx):
    server_id = ctx.message.server.id
    PLAYERS[server_id].stop()

@client.command(pass_context=True)
async def queue(ctx, url):
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    player = await voice_client.create_ytdl_player(url, after=lambda: check_queue(server.id))

    if server.id in QUEUES:
        QUEUES[server.id].append(player)
    else:
        QUEUES[server.id] = [player]
    await client.say('Music has been queued')

def check_queue(id):
    if QUEUES[id] != []:
        player = QUEUES[id].pop(0)
        PLAYERS[id] = player
        player.start()

def main():
    """Entrypoint if called as an executable."""
    args = parse_arguments()
    logging.basicConfig(level=logging.INFO)
    coloredlogs.install(level=0,
                        fmt="[%(asctime)s][%(levelname)s] [%(name)s.%(funcName)s:%(lineno)d] %(message)s",
                        isatty=True)
    if args.debug:
        l_level = logging.DEBUG
    else:
        l_level = logging.INFO
    logging.getLogger(__package__).setLevel(l_level)
    logging.getLogger('discord').setLevel(l_level)
    logging.getLogger('websockets.protocol').setLevel(l_level)
    LOG.info("LONG LIVE TAMAGO")
    TOKEN = os.getenv('TOKEN')

    client.loop.create_task(change_status())
    client.loop.create_task(list_servers())
    client.run(TOKEN)

if __name__ == "__main__":
    main()
