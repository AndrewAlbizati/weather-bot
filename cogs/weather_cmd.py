import discord
from discord.ext import commands
import requests
from weather import Weather


class WeatherCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(description="Sends weather and forecast.")
    @discord.option("city", description="Enter a city name")
    async def weather(self, ctx, city: str):
        w = self.get_data_from_city(city)

        if w is None:
            embed = discord.Embed(color=0xcf0000)
            embed.title = "Error"
            embed.description = f"\"{city}\" not found, please try again with a different name/spelling."

            await ctx.respond(embed=embed)
            return

        embed = discord.Embed()
        embed.title = "Weather in " + ' '.join(word.capitalize() for word in city.split(" "))
        embed.set_footer(text=f"{w.lat}, {w.lon}")

        await ctx.respond(embed=embed)

    def get_data_from_city(self, city_name):
        weather_base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&units=imperial&appid={self.bot.weather_api_key}"
        weather_res = requests.get(weather_base_url).json()

        if weather_res["cod"] != 200:
            return None

        lat = weather_res["coord"]["lat"]
        lon = weather_res["coord"]["lon"]

        forecast_base_url = f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&units=imperial&appid={self.bot.weather_api_key}"
        forecast_res = requests.get(forecast_base_url).json()
        if "cod" in forecast_res:
            return None

        return Weather(weather_res, forecast_res)


def setup(bot):
    bot.add_cog(WeatherCommand(bot))
