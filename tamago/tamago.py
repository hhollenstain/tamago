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
        #self.redis_url = kwargs.get('redis_url')
        self.dd_agent_url = kwargs.get('dd_agent_url')
        # self.db = Db(self.redis_url, self.mongo_url, self.loop)
        self.stats = DDAgent(self.dd_agent_url)

    # def run(self, *args):
    #     self.loop.run_until_complete(self.start(*args))

    async def on_ready(self):
        """Called when the bot is ready.

        Connects to the database
        Dispatched all the ready events

        """
        log.info('Connected to the database')

    async def send_message(self, *args, **kwargs):
        self.stats.incr('mee6.sent_messages')
        return await super().send_message(*args, **kwargs)

    async def on_message(self, message):
        self.stats.incr('mee6.recv_messages')
        if message.channel.is_private:
            return

        #await self.process_commands(message)

    # async def on_message_edit(self, before, after):
    #     if before.channel.is_private:
    #         return
    #
    #     server = after.server
    #     enabled_plugins = await self.get_plugins(server)
    #     for plugin in enabled_plugins:
    #         self.loop.create_task(plugin.on_message_edit(before, after))

    # async def on_message_delete(self, message):
    #     if message.channel.is_private:
    #         return
    #
    #     server = message.server
    #     enabled_plugins = await self.get_plugins(server)
    #     for plugin in enabled_plugins:
    #         self.loop.create_task(plugin.on_message_delete(message))

    # async def on_channel_create(self, channel):
    #     if channel.is_private:
    #         return
    #
    #     server = channel.server
    #     enabled_plugins = await self.get_plugins(server)
    #     for plugin in enabled_plugins:
    #         self.loop.create_task(plugin.on_channel_create(channel))

    # async def on_channel_update(self, before, after):
    #     if before.is_private:
    #         return
    #
    #     server = after.server
    #     enabled_plugins = await self.get_plugins(server)
    #     for plugin in enabled_plugins:
    #         self.loop.create_task(plugin.on_channel_update(before, after))

    # async def on_channel_delete(self, channel):
    #     if channel.is_private:
    #         return
    #
    #     server = channel.server
    #     enabled_plugins = await self.get_plugins(server)
    #     for plugin in enabled_plugins:
    #         self.loop.create_task(plugin.on_channel_delete(channel))
    #
    # async def on_member_join(self, member):
    #     server = member.server
    #     enabled_plugins = await self.get_plugins(server)
    #     for plugin in enabled_plugins:
    #         self.loop.create_task(plugin.on_member_join(member))

    # async def on_member_remove(self, member):
    #     server = member.server
    #     enabled_plugins = await self.get_plugins(server)
    #     for plugin in enabled_plugins:
    #         self.loop.create_task(plugin.on_member_remove(member))
    #
    # async def on_member_update(self, before, after):
    #     server = after.server
    #     enabled_plugins = await self.get_plugins(server)
    #     for plugin in enabled_plugins:
    #         self.loop.create_task(plugin.on_member_update(before, after))
    #
    # async def on_server_update(self, before, after):
    #     server = after
    #     enabled_plugins = await self.get_plugins(server)
    #     for plugin in enabled_plugins:
    #         self.loop.create_task(plugin.on_server_update(before, after))
    #
    # async def on_schwifty_playing(self, guild_id, url):
    #     server = discord.Object(id=str(guild_id))
    #     enabled_plugins = await self.get_plugins(server)
    #     for plugin in enabled_plugins:
    #         self.loop.create_task(plugin.on_schwifty_playing(guild_id, url))
    #
    # async def on_schwifty_finished_playing(self, guild_id):
    #     server = discord.Object(id=str(guild_id))
    #     enabled_plugins = await self.get_plugins(server)
    #     for plugin in enabled_plugins:
    #         self.loop.create_task(plugin.on_schwifty_finished_playing(guild_id))
