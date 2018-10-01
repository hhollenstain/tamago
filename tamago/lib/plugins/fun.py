import discord
import random
from discord.ext import commands

class Fun:
    def __init__(self, client):
        self.client = client

    @commands.command(name='8ball',
                    description="Answers a yes/no question.",
                    brief="Answers from the beyond.",
                    aliases=['eight_ball', 'eightball', '8-ball'],
                    pass_context=True)
    async def eight_ball(self, ctx):
        possible_responses = [
            'That is a resounding no',
            'It is not looking likely',
            'Too hard to tell',
            'It is quite possible',
            'Definitely',
        ]
        await self.client.say(random.choice(possible_responses) + ", " + ctx.message.author.mention)

def setup(client):
   client.add_cog(Fun(client))
