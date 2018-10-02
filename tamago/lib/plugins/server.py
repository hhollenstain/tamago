import discord
import logging
from discord import Game
from discord.ext import commands

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

        embed.set_image(url='https://pbs.twimg.com/profile_images/536300196326412288/BiNSl6fJ_400x400.png')
        embed.set_author(name='Benidct Tamago')
        embed.set_thumbnail(url='https://kikusushi.ca/dynamic_content/product_images/5/x533_50befac8f6b00a5ec710a911b675a98b.jpg.pagespeed.ic.Zsju56w-VL.webp')
        embed.add_field(name='description', value='Bot is a WIP, have fun!', inline=False)

        await self.client.say(embed=embed)

def setup(client):
    client.add_cog(Server(client))
