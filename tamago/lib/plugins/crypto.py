import discord
import aiohttp
import json
import logging
from discord.ext import commands

LOG = logging.getLogger(__name__)

class Crypto:
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def bitcoin(self):
        url = 'https://api.coindesk.com/v1/bpi/currentprice/BTC.json'
        async with aiohttp.ClientSession() as session:  # Async HTTP request
            raw_response = await session.get(url)
            response = await raw_response.text()
            response = json.loads(response)
            await self.client.say("Bitcoin price is: $" + response['bpi']['USD']['rate'])

def setup(client):
   client.add_cog(Crypto(client))
