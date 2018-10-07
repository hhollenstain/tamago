import discord
import logging
import os
import asyncio
import aiohttp
import json
#from database import Db
from discord.ext.commands import Bot
from tamago.lib.datadog import DDAgent

log = logging.getLogger('discord')


class Tamago(discord.ext.commands.Bot):
    """A modified discord.Client class

    This mod dispatches most events to the different plugins.

    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dd_agent_url = kwargs.get('dd_agent_url')
        self.owm_api_key = kwargs.get('owm_api_key')
        self.stats = DDAgent(self.dd_agent_url)

    async def send_message(self, *args, **kwargs):
        self.stats.incr('mee6.sent_messages')
        return await super().send_message(*args, **kwargs)
