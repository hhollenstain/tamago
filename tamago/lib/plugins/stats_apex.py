import discord
import logging
from discord.ext import commands
from apex_legends import AsyncLegends
from apex_legends.domain import Platform
from tamago.lib  import utils

LOG = logging.getLogger(__name__)

KWARGS = { 'pc': {'kwarg': 'platform',
                  'value': 'pc'},
           'psn': {'kwarg': 'platform',
                   'value': 'psn'},
           'xbox': {'kwarg': 'platform',
                    'value': 'xbox'},
           'comp': {'kwarg': 'mode',
                    'value': 'competitive'},
           'competitive': {'kwarg': 'mode',
                           'value': 'competitive'},
           'kd': {'kwarg': 'comparison_type',
                   'value': 'Eliminations per Life'},
           'qp': {'kwarg': 'mode',
                  'value': 'quickplay'},
           'qpc': {'kwarg': 'mode',
                   'value': 'quickplay,competitive'},
           'quickplay': {'kwarg': 'mode',
                         'value': 'quickplay'},
           'time': {'kwarg': 'comparison_type',
                    'value': 'Time Played'},
           'wins': {'kwarg': 'comparison_type',
                    'value': 'Games Won'},
           'winrate': {'kwarg': 'comparison_type',
                     'value': 'Win Percentage'},
}
KWARGS_DEFAULT = {
                  'platform': 'pc',
                 }

class StatsApex:
    def __init__(self, client):
        self.client = client

    def apexClient(self):
        api_key = self.tamago.apex_api_key
        if not api_key:

        AsyncLegends()
        return apexClient
    async def player(api_key, player_name, platform=None):
        async with AsyncLegends(api_key) as apex:
            player = await apex.player(player_name, platform=platform if platform else Platform.PC)
        return player

    @commands.command()
    @utils.block_check()
    async def apex(self, ctx, player, *args ):
        kwargs = kwarg_generator(args)
        LOG.info(kwargs)
        apex_data = await ow_load_data(player,
                        platform=kwargs['platform'],
                        comparison_type=kwargs['comparison_type'],
                        top=kwargs['top'],
                        modes=kwargs['mode'].split(','))
        if apex_data:
            embed = await stat_embed(ow_data)
            await ctx.send(embed=embed)
        else:
            await ctx.send(':information_source: Did not pass in a search paramater use !owhelp')

    @commands.command()
    @utils.block_check()
    async def apexhelp(self, ctx):
        help_dict = {}
        for arg in KWARGS:
            kwarg = '**{}**'.format(KWARGS[arg]['kwarg'])
            if kwarg not in help_dict:
                help_dict[kwarg] = []
            help_dict[kwarg].append(arg)

        embed = discord.Embed(
            title = ':information_source: Apex command help!',
            colour = discord.Colour.purple()
        )
        for kwarg in help_dict:
            embed.add_field(name=kwarg.upper(),
                            value=yaml.dump(help_dict[kwarg],
                                            default_flow_style=False,
                                            allow_unicode=True, indent=8),
                            inline=False)

        await ctx.send(embed=embed)

def kwarg_generator(args, kwargs_map=KWARGS, kwargs_default=KWARGS_DEFAULT):
    kwargs = {}
    for arg in args:
        if arg in kwargs_map:
            kwargs[kwargs_map[arg]['kwarg']] = kwargs_map[arg]['value']
        if arg.isdigit():
            kwargs['top'] = arg

    for k_default in kwargs_default:
        if k_default not in kwargs:
            kwargs[k_default] = kwargs_default[k_default]

    return kwargs

def ow_data_formatter(data, comparison_type):
    if comparison_type == 'Time Played':
        data = data.replace('[','').replace(']','').replace("'", "").split()
        data = ''.join(data).replace(',', ' ')
    if comparison_type == 'Win Percentage':
        data = '{}%'.format(float(data) * 100)
    if comparison_type == 'Eliminations per Life':
        data = '{} k/d'.format(float(data))
    return data

async def stat_embed(data_dict):

    embed = discord.Embed(
        title = list(data_dict.keys())[0],
        colour = discord.Colour.red(),
    )

    for user in data_dict:
        for mode in data_dict[user]:
            stat_values = []
            for stat in data_dict[user][mode]:
                stat_values.append('{} : {}'.format(stat, data_dict[user][mode][stat]))
            embed.add_field(name=mode, value=yaml.dump(stat_values,
                                                       default_flow_style=False,
                                                       allow_unicode=True, indent=8).replace("'", ""),
                            inline=False)

    return embed


def setup(client):
    client.add_cog(StatsOverwatch(client))
