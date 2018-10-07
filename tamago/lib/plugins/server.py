import discord
import logging
from discord import Game
from discord.ext import commands
from tamago import VERSION

LOG = logging.getLogger(__name__)

class Server:
    def __init__(self, client):
        self.client = client

    async def on_ready(self):
        await self.client.change_presence(game=Game(name="with humans"))
        LOG.info('Logged in as {}'.format(self.client.user.name))

    async def on_command_error(self, error, ctx):
        msg_channel = ctx.message.channel
        if isinstance(error, commands.CommandInvokeError):
            LOG.error(error)
            await self.client.send_message(msg_channel, '{} Error running the command'.format(ctx.message.author.mention))
        if isinstance(error, commands.CommandNotFound):
            await self.client.send_message(msg_channel, '{} the command you ran does not exist please use !help for assistance'.format(ctx.message.author.mention))

    @commands.command()
    async def tamago(self):
        embed = discord.Embed(
            title = 'Tamago Bot',
            description = 'Tamago Bot information',
            colour = discord.Colour.gold()
        )

        embed.set_author(name='Benidct Tamago')
        embed.set_thumbnail(url='https://pbs.twimg.com/profile_images/536300196326412288/BiNSl6fJ_400x400.png')
        embed.add_field(name='description', value='Bot is a WIP, have fun! Use !help for commands', inline=True)
        embed.add_field(name='Version', value=VERSION, inline=True)

        await self.client.say(embed=embed)

def setup(client):
    client.add_cog(Server(client))
