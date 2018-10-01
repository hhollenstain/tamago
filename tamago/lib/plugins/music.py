import discord
import logging
import youtube_dl
from discord.ext import commands

LOG = logging.getLogger(__name__)

PLAYERS = {}
QUEUES = {}

class Music:
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True)
    async def play(self, ctx, url):
        opts = {
         'default_search': 'auto',
         'quiet': True,
        }
        before_options = '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 2'

        server = ctx.message.server
        if server.id in PLAYERS:
             LOG.info("stopping current player before second player starts")
             PLAYERS[server.id].stop()

        voice_client = self.client.voice_client_in(server)
        player = await voice_client.create_ytdl_player(url,
                                                       ytdl_options=opts,
                                                       before_options=before_options,
                                                       after=lambda: check_queue(server.id))
        PLAYERS[server.id] = player
        player.start()

    @commands.command(pass_context=True)
    async def pause(self, ctx):
        server_id = ctx.message.server.id
        PLAYERS[server_id].pause()

    @commands.command(pass_contex=True)
    async def resume(self, ctx):
        server_id = ctx.message.server.id
        PLAYERS[server_id].resume()

    @commands.command(pass_contex=True)
    async def stop(self, ctx):
        LOG.info('STOPING?')
        server_id = ctx.message.server.id
        PLAYERS[server_id].stop()

    @commands.command(pass_context=True)
    async def queue(self, ctx, url):
        opts = {
         'default_search': 'auto',
         'quiet': True,
        }
        before_options = '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 2'

        server = ctx.message.server
        voice_client = self.client.voice_client_in(server)
        player = await voice_client.create_ytdl_player(url,
                                                       ytdl_options=opts,
                                                       before_options=before_options,
                                                       after=lambda: check_queue(server.id))

        if server.id in QUEUES:
            QUEUES[server.id].append(player)
        else:
            QUEUES[server.id] = [player]
        await self.client.say('Music has been queued')

    def check_queue(id):
        if QUEUES[id] != []:
            player = QUEUES[id].pop(0)
            PLAYERS[id] = player
            player.start()

def setup(client):
   client.add_cog(Music(client))
