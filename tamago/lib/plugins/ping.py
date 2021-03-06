import discord
import logging
from discord.ext import commands
from tamago.lib  import utils

LOG = logging.getLogger(__name__)


# class Greetings(commands.Cog):
#     def __init__(self, bot):
#         self.bot = bot
#         self._last_member = None

class Ping(commands.Cog):
    def __init__(self, client):
        self.client = client

    # async def on_message_delete(self, message):
    #     await self.client.send_message(message.channel, 'Message deleted.')

    @commands.command()
    @utils.block_check()
    async def ping(self, ctx):
        await ctx.send('Pong')

def setup(client):
    client.add_cog(Ping(client))
