import discord
import logging
import over_stats
import oyaml as yaml
from discord.ext import commands
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
                  'mode': 'competitive',
                  'comparison_type': None,
                  'top': 5,
                 }

class StatsOverwatch:
    def __init__(self, client):
        self.client = client

    @commands.command()
    @utils.block_check()
    async def ow(self, ctx, player, *args ):
        kwargs = kwarg_generator(args)
        LOG.info(kwargs)
        ow_data = await ow_load_data(player,
                           platform=kwargs['platform'],
                           comparison_type=kwargs['comparison_type'],
                           top=kwargs['top'],
                           modes=kwargs['mode'].split(','))
        if ow_data:
            embed = await stat_embed(ow_data)
            await ctx.send(embed=embed)
        else:
            await ctx.send(':information_source: Did not pass in a search paramater use !owhelp')

    @ow.error
    async def ow_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            if 'PlayerNotFound' in str(error):
                msg = ':mag: player not found check your user name'
            if not msg:
                msg = 'overwatch data overflow! Please reduce the query amount!'

            await ctx.send(msg)

    @commands.command()
    @utils.block_check()
    async def owhelp(self, ctx):
        help_dict = {}
        for arg in KWARGS:
            kwarg = '**{}**'.format(KWARGS[arg]['kwarg'])
            if kwarg not in help_dict:
                help_dict[kwarg] = []
            help_dict[kwarg].append(arg)

        embed = discord.Embed(
            title = ':information_source: Overwatch command help!',
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

    if kwargs['comparison_type'] == 'Win Percentage':
        kwargs['mode'] = 'competitive'

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


async def ow_load_data2(player, modes=['quickplay', 'competitive'],
                 platform='pc', comparison_type=None, top=5 ):
    ow_data = {}
    ow_stats = {}
    player_data = over_stats.PlayerProfile(player, platform)

    player_data.load_data()
    for mode in modes:
        ow_data[mode] = {}
        if comparison_type:
            for comparison_hero in player_data.comparison_heroes(mode, comparison_type):
                ow_data[mode][comparison_hero] = str(player_data.comparisons(mode, comparison_type, comparison_hero))
            stat = '**{} - {}**'.format(player, comparison_type)
            ow_stats[stat] = {}
            for mode in ow_data:
                ow_stats[stat]['**{}**'.format(mode.upper())] = {}
                for hero in utils.take(int(top), ow_data[mode]):
                    ow_stats[stat]['**{}**'.format(mode.upper())]['**{}**'.format(hero)] = ow_data_formatter(ow_data[mode][hero], comparison_type)

    return ow_stats

async def ow_load_data(player, modes=['quickplay', 'competitive'],
                 platform='pc', comparison_type=None, top=5 ):
    ow_data = {}
    ow_stats = {}
    player_data = over_stats.PlayerProfile(player, platform)
    player_data.load_data()
    for mode in modes:
        ow_data[mode] = {}
        if comparison_type:
            for comparison_hero in player_data.comparison_heroes(mode, comparison_type):
                ow_data[mode][comparison_hero] = str(player_data.comparisons(mode, comparison_type, comparison_hero))
            stat = '**{} - {}**'.format(player, comparison_type)
            ow_stats[stat] = {}
            for mode in ow_data:
                ow_stats[stat]['**{}**'.format(mode.upper())] = {}
                for hero in utils.take(int(top), ow_data[mode]):
                    ow_stats[stat]['**{}**'.format(mode.upper())]['{}'.format(hero)] = ow_data_formatter(ow_data[mode][hero], comparison_type)

    return ow_stats

def setup(client):
    client.add_cog(StatsOverwatch(client))
