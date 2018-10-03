import asyncio
import discord
import functools
import logging
import youtube_dl
from discord.ext import commands
from tamago.lib  import utils

LOG = logging.getLogger(__name__)

PLAYERS = {}
QUEUES = {}

class Music:
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True)
    async def play(self, ctx, *url):
        url = ' '.join(url)
        msg_channel = ctx.message.channel
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
        player_info = player.yt.extract_info(player.url, download=False)

        if "entries" in player_info:
            player_info = player_info['entries'][0]

        embed = discord.Embed(
            title = player.title,
            colour = discord.Colour.red(),
            description = player.description[:500]
        )
        embed.set_thumbnail(url=player_info['thumbnail'])
        embed.add_field(name='Uploaded by:', value=player.uploader, inline=True)
        embed.add_field(name='Duration:', value=utils.friendly_time(player.duration), inline=True)
        embed.add_field(name='URL:', value= player_info['webpage_url'])

        await self.client.say(embed=embed)
        player.start()

    @commands.command(pass_context=True)
    async def ms(self, ctx):
        server_id = ctx.message.server.id
        PLAYERS[server_id].stop()

    @commands.command(pass_context=True)
    async def pause(self, ctx):
        server_id = ctx.message.server.id
        PLAYERS[server_id].pause()

    @commands.command(pass_context=True)
    async def res(self, ctx):
        LOG.info('TRYING TO RESUME!')
        server_id = ctx.message.server.id
        PLAYERS[server_id].pause()

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
