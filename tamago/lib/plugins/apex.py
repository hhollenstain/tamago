import asyncio
import discord
import logging
from discord.ext import commands
from apex_legends import ApexLegends
from apex_legends import AsyncLegends
from apex_legends import exceptions as ApexExceptions
from apex_legends.domain import Platform
from tamago.lib import utils

LOG = logging.getLogger(__name__)

RANKS = (
    (0, 29, 'bronze4'),
    (30, 59, 'bronze3'),
    (60, 89, 'bronze2'),
    (90, 119, 'bronze1'),
    (120, 159, 'silver4'),
    (160, 199, 'silver3'),
    (200, 239, 'silver2'),
    (240, 279, 'silver1'),
    (280, 199, 'gold4'),
    (330, 199, 'gold3'),
    (380, 199, 'gold2'),
    (430, 199, 'gold1'),
    (480, 199, 'platinum4'),
    (540, 199, 'platinum3'),
    (600, 199, 'platinum2'),
    (660, 199, 'platinum1'),
    (720, 199, 'diamond4'),
    (790, 199, 'diamond3'),
    (860, 199, 'diamond2'),
    (930, 199, 'diamond1'),
    (1000, 20000, 'apex'),
    )

LEGENDS = [
           'bangalore',
           'bloodhound',
           'caustic',
           'gibraltar',
           'lifeline',
           'mirage',
           'octane',
           'pathfinder',
           'wattson',
           'wraith',
          ]


def rank_lookup(value, ranges):
    value = utils.to_int(value)
    left, right = 0, len(ranges)
    while left != right - 1:
        mid = left + (right - left) // 2
        if int(value) <= ranges[mid - 1][1]:  # Check left split max
            right = mid
        elif int(value) >= ranges[mid][0]:    # Check right split min
            left = mid
        else:                            # We are in a gap
            return None

    if ranges[left][0] <= int(value) <= ranges[left][1]:
        # Return the code
        return ranges[left][2]


class ApexUnkownPlayerError(commands.CommandError):
    """Custom Exception class for no players errors."""

class ApexPlayerSource:
    def __init__(self, tamago, player):
        self.tamago  = tamago

    async def apex_get_player(self, player):
        """
        returns Apex player object of requested player
        :param: object self: discord client
        :param: string player: player string
        :sends an apex player object
        """
        # try:
        #     async with AsyncLegends(self.tamago.apex_api_key) as apexData:
        #         player_data = await apexData.player(player, platform=Platform.PC)
        #     return player_data
        # except ApexExceptions.UnknownPlayerError:
        #   raise ApexUnkownPlayerError(f'Unknown Apex Player: {player}')
        try:
            apex = ApexLegends(self.tamago.apex_api_key)
            player_data = apex.player(player, platform=Platform.PC)
            return player_data
        except ApexExceptions.UnknownPlayerError:
          raise ApexUnkownPlayerError(f'Unknown Apex Player: {player}')

    async def apex_get_legends(self, player):
        """
        returns Apex player legends object of requested player
        :param: object self: discord client
        :param: string player: player string
        :sends an apex player legends object
        """
        # try:
        #     async with AsyncLegends(self.tamago.apex_api_key) as apexData:
        #         player_data = await apexData.player(player, platform=Platform.PC)
        #     return player_data.legends
        # except ApexExceptions.UnknownPlayerError:
        #   raise ApexUnkownPlayerError(f'Unknown Apex Player: {player}')
        try:
            apex = ApexLegends(self.tamago.apex_api_key)
            player_data = apex.player(player, platform=Platform.PC)
            return player_data.legends
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
        player_info = await self.parse(player)
        player_data = await ApexPlayerSource.apex_get_player(self, player_info['player'])
        embed = discord.Embed(
            title = f'Stats for {player.upper()}',
            url = f'https://apex.tracker.gg/profile/pc/{player_info["player"]}',
            colour = discord.Colour.purple()
        )

        embed.add_field(name="**Level**", value=f'{player_data.level}', inline=False)
        embed.add_field(name="**Rank**", value=f'{player_data.rankscore} ({rank_lookup(player_data.rankscore,RANKS)})', inline=True)
        embed.add_field(name="**Kills**", value=f'{player_data.kills}', inline=False)
        embed.add_field(name="**Damage**", value=f'{player_data.damage}', inline=True)
        embed.set_thumbnail(url=f'https://trackercdn.com/cdn/apex.tracker.gg/ranks/{rank_lookup(player_data.rankscore,RANKS)}.png')

        await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    @utils.block_check()
    async def apexlegends(self, ctx, *, info: str=''):
        """
        prints a discord embed with apex stats details of requested player
        :param: object self: discord client
        :param: dict   ctx: dictionary of message passed
        :param: string player: player string
        :sends an embed discord message of player stats
        """
        player_data = await self.parse(info)
        if not player_data['player']:
            raise ApexUnkownPlayerError(f'No player provided')

        legend_data = await ApexPlayerSource.apex_get_legends(self, player_data['player'])
        legend_embed_data = {}
        if player_data['legends']:
            for legend in player_data['legends']:
                legend_embed_data[legend] = {}
                try:
                    current_legend_filter = filter(lambda x: x.legend_name.lower() == legend, legend_data)
                    current_legend = next(current_legend_filter)
                    for meta in current_legend._stats:
                        legend_embed_data[legend][meta['metadata']['name']] = meta['value']
                except StopIteration:
                    legend_embed_data[legend]['error'] = f'Legend for {player_data["player"]}, please update at `https://apex.tracker.gg/`'


        embed = discord.Embed(
            title = f'Legends for {player_data["player"]}',
            colour = discord.Colour.orange()
        )

        for legend in legend_embed_data:
            embed.add_field(name='Legend', value=legend.upper(), inline=False)
            for stat in legend_embed_data[legend]:
                embed.add_field(name=stat.upper(), value=legend_embed_data[legend][stat], inline=True)

        if len(player_data['legends']) == 1:
            embed.set_thumbnail(url=f'{current_legend.bgimage}')


        await ctx.send(embed=embed)

    async def parse(self, message):
        legends = []
        player = None
        message = message.lower().split()
        data = {}
        for info in message:
            if info in LEGENDS:
                legends.append(info)
            if info not in LEGENDS:
                player = info
        data['player'] = player
        data['legends'] = legends
        return data


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
