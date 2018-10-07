import discord
import logging
import pyowm
from discord.ext import commands

LOG = logging.getLogger(__name__)

def get_emoji(status):
    """
    Returns the discord emoji code for the weather Status
    :param string status: weather status that maps to the emoji status dictionary
    :return: emoji code for Discord
    :rtype: string
    """
    emoji_status = {
                    'broken clouds': ':cloud:',
                    'Clear': ':sunny:',
                    'Clouds': ':cloud:',
                    'light rain': ':cloud_rain:',
                    'mist': ':cloud_rain:',
                    'Rain': ':cloud_rain:',
                    'scattered clouds': ':cloud:',
                    'Thunderstorm': ':cloud_lightning:',
                   }

    if status in emoji_status:
        return emoji_status[status]
    else:
        return status

def get_weather(location, owm_api_key):
    """
    Gets weather data from Openweathermaps api
    :param string location: location to search for weather
    :param string owm_api_key: api key to use
    :return: Returns weather information in a dictionary
    :rtype: dictionary
    """
    degree_sign= u'\N{DEGREE SIGN}'
    owm = pyowm.OWM(owm_api_key)
    weather = {}

    try:
        w = owm.weather_at_place(location).get_weather()
    except pyowm.exceptions.api_response_error.NotFoundError:
        weather['ERROR'] = {'value': 'Unable to find location, try another', 'inline': True }
        return weather

    weather['Status'] = {'value': get_emoji(w.get_status()), 'inline': True }
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
    weather['Rain'] = {'value': w.get_rain(), 'inline': False }
    weather['Snow'] = {'value': w.get_snow(), 'inline': False }

    return weather

class Weather:
    def __init__(self, tamago):
        self.tamago = tamago

    @commands.command(pass_context=True)
    async def weather(self, ctx, *location):
        """
        prints a discord embed with weather details of requested location
        :param: object self: discord client
        :param: dict   ctx: dictionary of message passed
        :param: string location: location string either name of place or zipcode
        :sends an embed discord message of weather values
        """
        location = ' '.join(location)
        embed = discord.Embed(
            title = 'Weather for {}'.format(location),
            colour = discord.Colour.blue()
        )

        weatherDict = get_weather(location, self.tamago.owm_api_key)

        for weatherValue in weatherDict:
            if weatherDict[weatherValue]['value']:
                embed.add_field(name=weatherValue, value=weatherDict[weatherValue]['value'], inline=weatherDict[weatherValue]['inline'])

        await self.tamago.say(embed=embed)

def setup(tamago):
    tamago.add_cog(Weather(tamago))
