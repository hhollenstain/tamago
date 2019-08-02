import asyncio
import argparse
import discord
import logging
import os
from discord import Game
from itertools import cycle, islice
from tamago import VERSION
from discord.ext import commands

LOG = logging.getLogger(__name__)
BLOCKED_USERS = os.getenv('BLOCKED_USERS') or '123456'

def to_int(value):
    if isinstance(value, str):
        return int(value.replace(",", ""))
    else:
        return value

def parse_arguments():
    """parsing arguments.

    """
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--debug', help='enable debug', action='store_true')
    parser.add_argument('--version', action='version',
                        version=format(VERSION),
                        help='show the version number and exit')

    return parser.parse_args()

def take(n, iterable):
    "Return first n items of the iterable as a list"
    return list(islice(iterable, n))

def friendly_time(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)

    periods = [('hours', hours), ('minutes', minutes), ('seconds', seconds)]
    time_string = ', '.join('{} {}'.format(value, name)
                            for name, value in periods
                            if value)

    return '{}'.format(time_string)

def message_check(message, mentions):
    return message.author.id in mentions

def block_check():
    def predicate(ctx):
        if str(ctx.message.author.id) in BLOCKED_USERS:
            return False
        else:
            return True
    return commands.check(predicate)

async def change_status(client):
    await client.wait_until_ready()

    if os.environ.get('GAMES') is not None:
        GAMES = os.environ.get('GAMES').split(",")
        sts = cycle(GAMES)

        while not client.is_closed():
            current_status = next(sts)
            await client.change_presence(status=discord.Status.idle, activity=Game(name=current_status))
            await asyncio.sleep(10)
    else:
        while not client.is_closed():
            guild_count = len(client.guilds)
            current_status = 'Serving {} Discord servers!'.format(guild_count)
            await client.change_presence(status=discord.Status.idle, activity=Game(name=current_status))
            await asyncio.sleep(60)


async def list_servers(client):
    await client.wait_until_ready()
    while not client.is_closed():
        server_list = []
        for server in client.guilds:
            server_list.append(server.name)
        LOG.info('Current servers: {}'.format(server_list))
        await asyncio.sleep(600)
