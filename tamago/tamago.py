#!/usr/bin/env python3
"""
Tamago BOT LIVES!
"""
import asyncio
import random
import os
import discord
import importlib
import logging
import coloredlogs
import sys
from discord import Game
from discord.ext import commands
from discord.ext.commands import Bot
from tamago.lib import plugin, utils


EXTENSIONS = [
             'tamago.lib.plugins.crypto',
             'tamago.lib.plugins.fun',
             # 'tamago.lib.plugins.help',
             'tamago.lib.plugins.mod_tools',
             'tamago.lib.plugins.music',
             'tamago.lib.plugins.ping',
             #'tamago.lib.plugins.reactions',
             'tamago.lib.plugins.server',
             #'tamago.lib.plugins.voice',
             'tamago.lib.plugins.fart',
             ]

LOG = logging.getLogger(__name__)
BOT_PREFIX = ("?", "!")
client = Bot(command_prefix=BOT_PREFIX)

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('expresso'):
        msg = 'https://scontent-sea1-1.xx.fbcdn.net/v/t1.0-9/5018_110506398392_7227641_n.jpg?_nc_cat=103&oh=09d93ddbb2a1d5f653895ba67b71845b&oe=5C5AA237'.format(message)
        await client.send_message(message.channel, msg)

    await client.process_commands(message)

def main():
    """Entrypoint if called as an executable."""
    args = utils.parse_arguments()
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

    client.loop.create_task(utils.change_status(client))
    client.loop.create_task(utils.list_servers(client))
    client.run(TOKEN)

if __name__ == '__main__':
    main()
