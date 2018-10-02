import discord
import logging
from discord.ext import commands

LOG = logging.getLogger(__name__)

class Reactions:
    def __init__(self, client):
        self.client = client

    async def on_reaction_add(self, reaction, user):
        channel = reaction.message.channel
        await self.client.send_message(channel, '{} has added {} to the message: {}'.format(user.name, reaction.emoji, reaction.message.content))

    async def on_reaction_remove(self, reaction, user):
        channel = reaction.message.channel
        await self.client.send_message(channel, '{} has remmoved {} to the message: {}'.format(user.name, reaction.emoji, reaction.message.content))

def setup(client):
    client.add_cog(Reactions(client))
