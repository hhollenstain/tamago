import discord
import logging
from discord.ext import commands

LOG = logging.getLogger(__name__)

class ModTools:
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True)
    @commands.has_permissions(manage_messages=True, administrator=True)
    async def clear(self, ctx, amount=5):
        LOG.info
        channel = ctx.message.channel
        messages = []
        async for message in self.client.logs_from(channel, limit=int(amount) + 1):
            messages.append(message)
        await self.client.delete_messages(messages)
        await self.client.say('%s messages purged' % amount)

def setup(client):
    client.add_cog(ModTools(client))
