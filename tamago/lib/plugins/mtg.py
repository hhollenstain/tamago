import requests
import discord
from discord.ext import commands

CARD_FACES = "card_faces"
CREATURE = "Creature"
DATA = "data"
DOLLAR_SIGN = "$"
EMPTY_STRING = ""
FLIP = "flip"
FORWARD_SLASH = "/"
FUZZY_SEARCH = "https://api.scryfall.com/cards/named?fuzzy=%s"
LAYOUT = "layout"
MANA_COST = "mana_cost"
MELD = "meld"
NAME = "name"
NEW_LINE = "\n"
NORMAL = "normal"
NOT_AVAILABLE = "N/A"
ORACLE_TEXT = "oracle_text"
PARENTHESIS_LEFT = "("
PARENTHESIS_RIGHT = ")"
PLUS = "+"
POWER = "power"
PRICES = "prices"
PRINTS_SEARCH_URI = "prints_search_uri"
SAGA = "saga"
SET = "set"
SET_NAME = "set_name"
SPACE = " "
SPLIT = "split"
TAB = "\t"
TOUGHNESS = "toughness"
TRANSFORM = "transform"
TRANSFORM_LINE_BREAK = "---------"
TYPE_LINE = "type_line"
USD = "usd"
USD_FOIL = "usd_foil"


class Card(commands.Cog):
    def __init__(self, tamago):
        self.tamago = tamago

    @staticmethod
    def price(*args):
        plus_delimited_card_name = Card.__get_plus_delimited_card_name(*args)

        response = requests.get(FUZZY_SEARCH % plus_delimited_card_name)
        card_layout = Card.__get_card_layout(response)

        #return f'{Card.__print_card_header(response, card_layout)} {Card.__print_card_price(response)}'
        return Card.__print_card_price(response)

    @staticmethod
    def search(*args):
        plus_delimited_card_name = Card.__get_plus_delimited_card_name(*args)

        response = requests.get(FUZZY_SEARCH % plus_delimited_card_name)
        card_layout = Card.__get_card_layout(response)

        return f'{Card.__print_card_header(response, card_layout)} {Card.__print_card_search(response, card_layout)}'

    @commands.command()
    async def mtg(self, ctx, *, info: str = ''):
        info = info.lower().split(" ", 1)

        embed = None

        if info[0] == "search":
            card_info = self.search(info[1])

            embed = discord.Embed(
                title=f'\u200b',
                colour=discord.Colour.dark_red()
            )
            embed.add_field(name=f'\u200b', value=card_info)
            await ctx.send(embed=embed)

        elif info[0] == "price":
            cards = self.price(info[1])

            embed = discord.Embed(
                title=f'MTG Prices              Normal/Foil',
                colour=discord.Colour.purple()
            )

            # embed.add_field(name=f'Set Name', inline=True)
            # embed.add_field(name=f'Normal', inline=True)
            # embed.add_field(name=f'Foil', inline=True)

            i = 1
            efsn = []
            efp = []
            for card in cards:
                if i % 5 == 0:

                    embed.add_field(name=f'\u200b', value='\n'.join(efsn), inline=True)
                    embed.add_field(name=f'\u200b', value='\n'.join(efp), inline=True)
                    #embed.add_field(name=f'\u200b', value=f'\u200b', inline=False)
                    await ctx.send(embed=embed)
                    i = 1
                    embed = discord.Embed(
                        title=f'MTG Prices              Normal/Foil',
                        colour=discord.Colour.purple()
                    )
                    efsn = []
                    efp = []
                else:
                    efsn.append(f'{cards[card]["set_name"]}\n')
                    efp.append(f'{DOLLAR_SIGN}{cards[card]["normal_price"]}{SPACE}{FORWARD_SLASH}'
                               f'{SPACE}{DOLLAR_SIGN}{cards[card]["foil_price"]}\n')
                    i += 1

            if efsn:
                embed.add_field(name=f'\u200b', value='\n'.join(efsn), inline=True)
                embed.add_field(name=f'\u200b', value='\n'.join(efp), inline=True)
                await ctx.send(embed=embed)







    @staticmethod
    def __get_card_description(response, card_layout):
        description = EMPTY_STRING

        info = {}

        if card_layout == NORMAL or card_layout == MELD or card_layout == SAGA:
            if CREATURE in response.json()[TYPE_LINE]:
                info['TYPE_LINE'] = response.json()[TYPE_LINE]
                info['ORACLE_TEXT'] = response.json()[ORACLE_TEXT]
                info['POWER_TOUGHNESS'] = response.json()[POWER] + SPACE + FORWARD_SLASH + SPACE + \
                                          response.json()[TOUGHNESS]
            else:
                info['TYPE_LINE'] = response.json()[TYPE_LINE]
                info['ORACLE_TEXT'] = response.json()[ORACLE_TEXT]
        elif card_layout == TRANSFORM or card_layout == SPLIT or card_layout == FLIP:
            if CREATURE in response.json()[TYPE_LINE]:
                info['TYPE_LINE'] = response.json()[CARD_FACES][0][TYPE_LINE]
                info['ORACLE_TEXT'] = response.json()[CARD_FACES][0][ORACLE_TEXT]
                info['POWER_TOUGHNESS'] = response.json()[CARD_FACES][0][POWER] + SPACE + FORWARD_SLASH + SPACE + \
                                    response.json()[CARD_FACES][0][TOUGHNESS]
                info['B_TYPE_LINE'] = response.json()[CARD_FACES][0][TYPE_LINE]
                info['B_ORACLE_TEXT'] = response.json()[CARD_FACES][1][ORACLE_TEXT]
                info['B_POWER_TOUGHNESS'] = response.json()[CARD_FACES][1][POWER] + SPACE + FORWARD_SLASH + SPACE + \
                                   response.json()[CARD_FACES][1][TOUGHNESS]
            else:
                info['TYPE_LINE'] = response.json()[CARD_FACES][0][TYPE_LINE]
                info['ORACLE_TEXT'] = response.json()[CARD_FACES][0][ORACLE_TEXT]
                info['B_TYPE_LINE'] = response.json()[CARD_FACES][0][TYPE_LINE]
                info['B_ORACLE_TEXT'] = response.json()[CARD_FACES][1][ORACLE_TEXT]



        return info

    @staticmethod
    def __get_card_layout(response):
        return response.json()[LAYOUT]

    @staticmethod
    def __get_card_mana_cost(response, card_layout):
        mana_cost = EMPTY_STRING

        if card_layout == NORMAL or card_layout == MELD or card_layout == SAGA:
            mana_cost = response.json()[MANA_COST]
        elif card_layout == TRANSFORM or card_layout == FLIP:
            mana_cost = response.json()[CARD_FACES][0][MANA_COST]
        elif card_layout == SPLIT:
            mana_cost = response.json()[CARD_FACES][0][MANA_COST] + \
                        SPACE + FORWARD_SLASH + FORWARD_SLASH + SPACE + response.json()[CARD_FACES][1][MANA_COST]

        return mana_cost

    @staticmethod
    def __get_card_name(response):
        return response.json()[NAME]

    # TODO: Refactor this method name into something else since it is technically getting both set and prices.
    @staticmethod
    def __get_card_set_names(response):
        card_set_list = dict()
        prints_search_uri = response.json()[PRINTS_SEARCH_URI]

        card_sets_response = requests.get(prints_search_uri)

        for json in card_sets_response.json()[DATA]:
            set_name = json[SET_NAME]
            set_code = json[SET].upper()
            normal_price = json[PRICES][USD]
            foil_price = json[PRICES][USD_FOIL]

            set_name = set_name + SPACE + PARENTHESIS_LEFT + set_code + PARENTHESIS_RIGHT

            card_set_list.update({set_name: [normal_price, foil_price]})

        return card_set_list

    @staticmethod
    def __get_plus_delimited_card_name(*args):
        plus_delimited_card_name = EMPTY_STRING

        for index, argument in enumerate(args):
            if index == len(args) - 1:
                plus_delimited_card_name = plus_delimited_card_name + argument
            else:
                plus_delimited_card_name = plus_delimited_card_name + argument + PLUS

        return plus_delimited_card_name

    @staticmethod
    def __print_card_header(response, card_layout):
        #print(Card.__get_card_name(response) + TAB + TAB + Card.__get_card_mana_cost(response, card_layout) + NEW_LINE)
        return f'{Card.__get_card_name(response) }   {Card.__get_card_mana_cost(response, card_layout) }'

    @staticmethod
    def __print_card_price(response):
       #strReturn=[]
        prices = {}
        i = 0
        for set_name, card_prices_usd in Card.__get_card_set_names(response).items():
            prices[set_name] = prices.get(set_name,{})
            prices[set_name]['set_name'] = set_name
           # prices[i]['set_name'] = set_name
            #print(TAB + set_name)
            if not card_prices_usd[0] is None:
                #normal_price = card_prices_usd[0]
                prices[set_name]['normal_price'] = card_prices_usd[0]
            else:
                prices[set_name]['normal_price'] = NOT_AVAILABLE
                #normal_price = NOT_AVAILABLE

            if not card_prices_usd[1] is None:
                #foil_price = card_prices_usd[1]
                prices[set_name]['foil_price'] = card_prices_usd[1]
            else:
                #foil_price = NOT_AVAILABLE
                prices[set_name]['foil_price'] = NOT_AVAILABLE

            #i += i


            #print(TAB + TAB + DOLLAR_SIGN + normal_price + SPACE + FORWARD_SLASH + SPACE + DOLLAR_SIGN + foil_price)
            #return f" {set_name} \n  {DOLLAR_SIGN}{normal_price} {FORWARD_SLASH} {DOLLAR_SIGN} {foil_price}"
            #strReturn.append(f" {set_name} {DOLLAR_SIGN}{normal_price} {FORWARD_SLASH} {DOLLAR_SIGN} {foil_price} {NEW_LINE}")

        return prices
     
    @staticmethod
    def __print_card_search(response, card_layout):
        return f'{Card.__get_card_description(response, card_layout)} {NEW_LINE}'


def setup(tamago):
    tamago.add_cog(Card(tamago))
