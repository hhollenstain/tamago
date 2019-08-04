#!/usr/bin/env python3
"""
Tamago BOT LIVES!
"""
import aiohttp
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
from tamago.tamago import Tamago

EXTENSIONS = [
    'apex',
    'crypto',
    'fun',
    'meme',
    'mod_tools',
    'mtg',
    'music',
    'ping',
    'pubg',
    'server',
    'stats_overwatch',
    'weather',
    ]

LOG = logging.getLogger(__name__)

APP_ID = os.getenv('APP_ID') or 'fakeid'
BOT_PREFIX = ("?", "!")
DD_AGENT_URL = os.getenv('DD_AGENT_URL')
OWM_API_KEY = os.getenv('OWM_API_KEY') or '123456'
APEX_API_KEY = os.getenv('APEX_API_KEY') or None
REDIS_URL = os.getenv('REDIS_URL')
SHARD = os.getenv('SHARD') or 0
SHARD_COUNT = os.getenv('SHARD_COUNT') or 1
TOKEN = os.getenv('TOKEN')


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
    logging.getLogger('urllib3').setLevel(l_level)

    LOG.info("LONG LIVE TAMAGO")
    tamago = Tamago(shard_id=int(SHARD), shard_count=int(SHARD_COUNT), redis_url=REDIS_URL,
                    dd_agent_url=DD_AGENT_URL, owm_api_key=OWM_API_KEY, command_prefix=BOT_PREFIX,
                    apex_api_key=APEX_API_KEY, app_id=APP_ID)

    for extension in EXTENSIONS:
        plugin.load('tamago.lib.plugins.{}'.format(extension), tamago)

    tamago.aiohttp = aiohttp.ClientSession(loop=tamago.loop)
    tamago.run(TOKEN)

if __name__ == '__main__':
    main()
