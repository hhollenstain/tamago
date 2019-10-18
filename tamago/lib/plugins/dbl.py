import dbl
import discord
from discord.ext import commands

import asyncio
import logging

LOG = logging.getLogger(__name__)

class DiscordBotsOrgAPI(commands.Cog):
    """Handles interactions with the discordbots.org API"""

    def __init__(self, autochannel):
        self.autochannel = autochannel
        self.token = self.autochannel.dbl_token 
        self.dblpy = dbl.Client(self.autochannel, self.token)
        self.updating = self.autochannel.loop.create_task(self.update_stats())

    async def update_stats(self):
        """This function runs every 30 minutes to automatically update your server count"""
        while not self.autochannel.is_closed():
            if self.token: 
                LOG.info('Attempting to post server count')
                try:
                    await self.dblpy.post_guild_count()
                    LOG.info('Posted server count ({})'.format(self.dblpy.guild_count()))
                except Exception as e:
                    LOG.exception('Failed to post server count\n{}: {}'.format(type(e).__name__, e))
                await asyncio.sleep(1800)
            else:
                LOG.info('Skipping DBL guild count, no API key')

def setup(autochannel):
    autochannel.add_cog(DiscordBotsOrgAPI(autochannel))