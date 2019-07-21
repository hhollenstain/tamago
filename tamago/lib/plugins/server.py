import discord
import logging
import random
from discord import Game
from discord.ext import commands
from tamago import VERSION
from tamago.lib import utils

LOG = logging.getLogger(__name__)

class Server(commands.Cog):
    def __init__(self, tamago):
        self.tamago = tamago

    async def on_ready(self):
        await self.tamago.change_presence(status=discord.Status.idle, activity=Game(name='Waking up, making coffee...'))
        LOG.info('Logged in as {}'.format(self.tamago.user.name))
        self.tamago.loop.create_task(utils.change_status(self.tamago))
        self.tamago.loop.create_task(utils.list_servers(self.tamago))

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            LOG.error(error)
            msg = '{} Error running the command'.format(ctx.message.author.mention)
        if isinstance(error, commands.CommandNotFound):
            msg = '{} the command you ran does not exist please use !help for assistance'.format(ctx.message.author.mention)
        if isinstance(error, commands.CheckFailure):
            msg = ':octagonal_sign: you do not have permission to run this command, {}'.format(ctx.message.author.mention)
        if isinstance(error, commands.MissingRequiredArgument):
            msg = 'Missing required argument: ```{}```'.format(error)

        if not msg:
            msg = 'Oh no, I have no idea what I am doing! {}'.format(error)


        await ctx.send('{}'.format(msg))

    @commands.command()
    async def tamago(self, ctx):
        embed = discord.Embed(
            title = 'Tamago Bot',
            description = 'Tamago Bot information',
            colour = discord.Colour.gold()
        )

        tamago_avatar = [
                         'https://i.imgur.com/NtDueT7.png',
                         'https://i.imgur.com/pzwv3Gs.png',
                         'https://i.imgur.com/khPDnT2.png',
                         'https://i.imgur.com/GEJjUD3.png',
                         'https://i.imgur.com/e4EyhfI.png',
                        ]

        embed.set_author(name='Benidct Tamago')
        embed.set_thumbnail(url=random.choice(tamago_avatar))
        embed.add_field(name='description', value=f'Tamago is a WIP, add Tamago to your server! [add me]( https://discordapp.com/oauth2/authorize?client_id={self.tamago.app_id}&scope=bot)', inline=True)
        embed.add_field(name='Version', value=VERSION, inline=True)

        await ctx.send(embed=embed)

def setup(tamago):
    tamago.add_cog(Server(tamago))
