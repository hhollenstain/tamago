import discord
import logging
import pyowm
from discord.ext import commands

LOG = logging.getLogger(__name__)

def get_emoji(status):
    emoji_status = {
                    'broken clouds': ':cloud:'
                   }

    if status in emoji_status:
        return emoji_status[status]
    else:
        return status

def get_weather(location, owm_api_key):
    degree_sign= u'\N{DEGREE SIGN}'
    owm = pyowm.OWM(owm_api_key)
    weather = {}

    try:
        w = owm.weather_at_place(location).get_weather()
    except pyowm.exceptions.api_response_error.NotFoundError:
        weather['ERROR'] = {'value': 'Unable to find location, try another', 'inline': True }
        return weather

    weather['Status'] = {'value': get_emoji(w.get_detailed_status()), 'inline': True }
    weather['Cloud Coverage'] = {'value': '{}%'.format(w.get_clouds()), 'inline': True }
    weather['Wind'] = {'value': '{} mph'.format(round(w.get_wind(unit='miles_hour')['speed'], 2)),
                       'inline': True }
    weather['Humidity'] = {'value': '{}%'.format(w.get_humidity()), 'inline': False }
    weather['Temp'] = {'value': '{}{}F'.format(w.get_temperature(unit='fahrenheit')['temp'],
                                               degree_sign), 'inline': True }
    weather['Temp High'] = {'value': '{}{}F'.format(w.get_temperature(unit='fahrenheit')['temp_max'],
                                                    degree_sign), 'inline': True }
    weather['Temp Low'] = {'value': '{}{}F'.format(w.get_temperature(unit='fahrenheit')['temp_min'],
                                                   degree_sign), 'inline': True }
    if w.get_rain():
        weather['Rain'] = {'value': w.get_rain(), 'inline': False }
    if w.get_snow():
        weather['Snow'] = {'value': w.get_snow(), 'inline': False }

    return weather

class Weather:
    def __init__(self, tamago):
        self.tamago = tamago

    @commands.command(pass_context=True)
    async def weather(self, ctx, location):
        embed = discord.Embed(
            title = 'Weather for {}'.format(location),
            colour = discord.Colour.blue()
        )

        weatherDict = get_weather(location, self.tamago.owm_api_key)

        for weatherValue in weatherDict:
            embed.add_field(name=weatherValue, value=weatherDict[weatherValue]['value'], inline=weatherDict[weatherValue]['inline'])

        await self.tamago.say(embed=embed)

def setup(tamago):
    tamago.add_cog(Weather(tamago))
