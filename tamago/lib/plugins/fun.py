import discord
import logging
import random
from discord.ext import commands
from tamago.lib import utils

LOG = logging.getLogger(__name__)

class Fun(commands.Cog):
    def __init__(self, tamago):
        self.tamago = tamago

    @commands.command(name='8ball',
                    description="Answers a yes/no question.",
                    brief="Answers from the beyond.",
                    aliases=['eight_ball', 'eightball', '8-ball'],
                    pass_context=True)
    @utils.block_check()
    async def eight_ball(self, ctx):
        possible_responses = [
            'That is a resounding no',
            'It is not looking likely',
            'Too hard to tell',
            'It is quite possible',
            'Definitely',
        ]
        await ctx.send('{}, {}'.format(random.choice(possible_responses),
                                       ctx.message.author.mention))

    @commands.command(pass_context=True)
    async def hello(self, ctx):
        await ctx.send('Hello {}'.format(ctx.message.author.mention))

    async def on_message(self, message):
        if message.author == self.tamago.user:
            return

        if message.content.startswith('expresso'):
            msg = 'https://scontent-sea1-1.xx.fbcdn.net/v/t1.0-9/5018_110506398392_7227641_n.jpg?_nc_cat=103&oh=09d93ddbb2a1d5f653895ba67b71845b&oe=5C5AA237'.format(message)
            await message.channel.send(msg)

def setup(tamago):
   tamago.add_cog(Fun(tamago))
