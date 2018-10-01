import discord
import logging
from discord.ext import commands

LOG = logging.getLogger(__name__)

class Voice:
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True)
    async def join(self, ctx):
        msg_channel = ctx.message.channel
        voice_channel = ctx.message.author.voice.voice_channel
        try:
            await self.client.join_voice_channel(voice_channel)
        except Exception as e:
            LOG.error(e)
            await self.client.send_message(msg_channel, '{} DERP! you are currently not in a voice channel, unable to join'.format(ctx.message.author.mention))

    @commands.command(pass_context=True)
    async def leave(self, ctx):
        msg_channel = ctx.message.channel
        server  = ctx.message.author.server
        if self.client.is_voice_connected(server):
            voice_client = self.client.voice_client_in(server)
            await voice_client.disconnect()
        else:
            await self.client.send_message(msg_channel, '{} Tamago BOT is currently not in a voice channel, can\'t disconnect!'.format(ctx.message.author.mention))

def setup(client):
   client.add_cog(Voice(client))
