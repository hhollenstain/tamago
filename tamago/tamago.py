#!/usr/bin/env python3
"""
Tamago BOT LIVES!
"""
import asyncio
import random
import os
import argparse
import discord
import importlib
import logging
import coloredlogs
import sys
from itertools import cycle
from . import VERSION
from discord import Game
from discord.ext import commands
from discord.ext.commands import Bot
from .lib import plugin
#from .lib import plugins


EXTENSIONS = [
             '.lib.plugins.crypto',
             '.lib.plugins.ping',
             '.lib.plugins.fun',
             '.lib.plugins.music',
             '.lib.plugins.voice',
             ]

LOG = logging.getLogger(__name__)
BOT_PREFIX = ("?", "!")
client = Bot(command_prefix=BOT_PREFIX)
#client.remove_command('help')

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

# @client.command(pass_context=True)
# async def help(ctx):
#     author = ctx.message.author
#
#     embed = discord.Embed(
#         colour = discord.Colour.orange()
#     )
#
#     embed.set_author(name='Help')
#     embed.add_field(name='!ping', value='Returns Pong!', inline=False)
#     embed.add_field(name='!8ball', value='Shakes Magic 8ball for answer', inline=False)
#
#     await client.send_message(author, embed=embed)


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

    for extension in EXTENSIONS:
        plugin.load(extension, client)

    client.loop.create_task(change_status())
    client.loop.create_task(list_servers())
    client.run(TOKEN)

if __name__ == '__main__':
    main()
