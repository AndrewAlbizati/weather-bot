import discord
from discord.ext import commands
from datetime import datetime
from weather_utils import Weather_Utils

class Weather(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        with open("tokens.txt", "r") as f:
            lines = f.readlines()
            lines = [line.rstrip() for line in lines]
            self.weather_utils = Weather_Utils(lines[1])

    @commands.command()
    async def weather(self, ctx):
        message = ctx.message
        
        location = message.content.lower()[9:]

        try:
            # Correct if user sent coordinates
            if len(location.replace(", ", ",").split(",")) == 2:
                location = location.replace(", ", ",")
    
                lat = float(location.split(",")[0])
                lon = float(location.split(",")[1])

                data = self.weather_utils.getSimpleWeather([lat, lon])      
            else:
                data = self.weather_utils.getSimpleWeather(location)
        except:
            await ctx.send("Location not found!")
            return
        
        # Find local time for location
        timestamp = datetime.utcfromtimestamp(data["dt"] + data["timezone"])
        date = timestamp.strftime("%I:%M:%S %p") # HH:MM:SS AM/PM
        
        # Create embed
        embedVar = discord.Embed(title = "Weather for " + message.content[9:] + " (" + date + " local time)", color = 0xad0808)
        embedVar.description = str(
        "Temp: **" + str(data["main"]["temp"]) + "** (" + str(data["main"]["temp_min"]) + " - " + str(data["main"]["temp_max"]) + ")\n"
        "Hum: **" + str(data["main"]["humidity"]) + "%**\n"
        "*" + str(data["weather"][0]["description"]).capitalize() + "*")
        
        embedVar.set_thumbnail(url="https://openweathermap.org/img/wn/" + data["weather"][0]["icon"] + "@2x.png")
        embedVar.set_footer(text=str(data["coord"]["lat"]) + ", " + str(data["coord"]["lon"]))

        await ctx.channel.send(embed = embedVar)
    
def setup(bot):
    bot.add_cog(Weather(bot))