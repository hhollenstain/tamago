import asyncio
import discord
import logging
from discord.ext import commands
from apex_legends import AsyncLegends
from apex_legends import exceptions as ApexExceptions
from apex_legends.domain import Platform
from tamago.lib import utils

LOG = logging.getLogger(__name__)


class ApexUnkownPlayerError(commands.CommandError):
    """Custom Exception class for no players errors."""

class ApexPlayerSource:
    def __init__(self, tamago, player):
        self.tamago  = tamago

    async def apex_get_player(self, player):
        LOG.info(f"{self.tamago.apex_api_key}, {player}")
        try:
            async with AsyncLegends(self.tamago.apex_api_key) as apexData:
                player_data = await apexData.player(player, platform=Platform.PC)
            return player_data
        except ApexExceptions.UnknownPlayerError:
          raise ApexUnkownPlayerError(f'Unknown Apex Player: {player}')


class Apex(commands.Cog):
    def __init__(self, tamago):
        self.tamago = tamago

    @commands.command(pass_context=True)
    @utils.block_check()
    async def apex(self, ctx, player):
        """
        prints a discord embed with apex stats details of requested player
        :param: object self: discord client
        :param: dict   ctx: dictionary of message passed
        :param: string player: player string
        :sends an embed discord message of player stats
        """
        embed = discord.Embed(
            title = 'Stats for {}'.format(player),
            colour = discord.Colour.purple()
        )
        player_data = await ApexPlayerSource.apex_get_player(self, player)
        embed.add_field(name="player-test", value=player_data)

        await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    @utils.block_check()
    async def apexlegends(self, ctx, player, *legends):
        """
        prints a discord embed with apex stats details of requested player
        :param: object self: discord client
        :param: dict   ctx: dictionary of message passed
        :param: string player: player string
        :sends an embed discord message of player stats
        """

        await ctx.send('This is for apexlegends')
        # embed = discord.Embed(
        #     title = 'Stats for {}'.format(player),
        #     colour = discord.Colour.purple()
        # )
        # player_data = await ApexPlayerSource.apex_get_player(self, player)
        # embed.add_field(name="player-test", value=player_data)
        #
        # await ctx.send(embed=embed)


    @apex.error
    async def apex_handler(self, ctx, error):
        embed = discord.Embed(
            title = 'Apex Stats error',
            colour = discord.Colour.red()
        )
        if isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == 'player':
                embed.add_field(name='Missing Player', value='Please input the player you wish to lookup')
                await ctx.send(embed=embed)
        else:
            msg = error
            await ctx.send(msg)

def setup(tamago):
    tamago.add_cog(Apex(tamago))
#
#
#
#
#
# my_api_key = 'https://apex.tracker.gg api key here'
#
#
# async def main(api_key, player_name, platform=None):
#     async with AsyncLegends(api_key) as apex:
#         player = await apex.player(player_name, platform=platform if platform else Platform.PC)
#     return player
#
# loop = asyncio.get_event_loop()
# result = loop.run_until_complete(main(my_api_key, player_name='NRG_dizzy'))
#
# print(result)
#
# for legend in result.legends:
#     print(legend.legend_name)
#     print(legend.icon)
#     print(getattr(legend, 'damage', 'Damage not found.'))
