import asyncio
import argparse
import discord
import logging
from discord import Game
from itertools import cycle
from tamago import VERSION

LOG = logging.getLogger(__name__)

def parse_arguments():
    """parsing arguments.

    """
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--debug', help='enable debug', action='store_true')
    parser.add_argument('--version', action='version',
                        version=format(VERSION),
                        help='show the version number and exit')
    return parser.parse_args()

def friendly_time(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)

    periods = [('hours', hours), ('minutes', minutes), ('seconds', seconds)]
    time_string = ', '.join('{} {}'.format(value, name)
                            for name, value in periods
                            if value)

    return '{}'.format(time_string)

async def change_status(client):
    status = ['God = Ginger', 'Expresso is lame!', 'Vern\'s woo']
    await client.wait_until_ready()
    sts = cycle(status)

    while not client.is_closed:
        current_status = next(sts)
        await client.change_presence(game=discord.Game(name=current_status))
        await asyncio.sleep(15)

async def list_servers(client):
    await client.wait_until_ready()
    while not client.is_closed:
        server_list = []
        for server in client.servers:
            server_list.append(server.name)
        LOG.info('Current servers: {}'.format(server_list))
        await asyncio.sleep(600)
