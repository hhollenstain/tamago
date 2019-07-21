import aiohttp
import asyncio
import discord
import io
import logging
from discord.ext import commands
from bs4 import BeautifulSoup
from tamago.lib import utils

LOG = logging.getLogger(__name__)

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()


async def fetch_bytes(session, url):
    async with session.get(url) as response:
        return io.BytesIO(await response.read())

class Meme(commands.Cog):
    def __init__(self, tamago):
        self.tamago = tamago

    @commands.command(pass_context=True)
    @utils.block_check()
    async def meme(self, ctx, *meme):
        """
        prints a discord embed with weather details of requested location
        :param: object self: discord client
        :param: dict   ctx: dictionary of message passed
        :param: string meme: Meme string
        :returns the meme image
        """

        async with aiohttp.ClientSession() as session:
            html = await fetch(session, f"http://knowyourmeme.com/search?q={meme}")

            soup = BeautifulSoup(html, "html.parser")
            memes_list = soup.find(class_="entry_list")

            if not memes_list:
                await ctx.send(f"no meme found for [{meme}]")
                return

            meme_path = memes_list.find("a", href=True)["href"]
            meme_url = "https://knowyourmeme.com%s" % meme_path

            html = await fetch(session, meme_url)
            soup = BeautifulSoup(html, "html.parser")

            image_url = soup.find("meta", attrs={"property": "og:image"})["content"]
            buffer = await fetch_bytes(session, image_url)

            filename = f"image.{image_url.rsplit('.')[-1]}"

            await ctx.send(file=discord.File(buffer, filename=filename))

def setup(tamago):
    tamago.add_cog(Meme(tamago))
