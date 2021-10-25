import discord
from discord.ext import commands
from weather_utils import Weather_Utils
from datetime import datetime
import asyncio

class FCast(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        with open("tokens.txt", "r") as f:
            lines = f.readlines()
            lines = [line.rstrip() for line in lines]
            self.weather_utils = Weather_Utils(lines[1])

    @commands.command()
    async def fcast(self, ctx):
        message = ctx.message

        location = message.content.lower()[7:]
        data = self.weather_utils.getForecast(location)

        # Correct if user sent coordinates
        if len(location.replace(", ", ",").split(",")) == 2:
            location = location.replace(",", " ")
            try:
                lat = float(location.split(" ")[0])
                lon = float(location.split(" ")[1])

                data = self.weather_utils.getForecast([lat, lon])
            except ValueError:
                pass

        day_descriptions = []

        # Create a list of all days with all info stored in dicts
        for dayData in data["daily"][:-1]:
            timestamp = datetime.fromtimestamp(dayData["dt"])

            day_name = timestamp.strftime("%A")

            temp = {}
            temp["name"] = day_name
            temp["icon"] = dayData["weather"][0]["icon"]

            temp["value"] = "Temp: **" + str(dayData["temp"]["day"]) + "F** (" + str(dayData["temp"]["min"]) + " - " + str(dayData["temp"]["max"]) +")\nHum: **" + str(dayData["humidity"]) + "%**\n*" + dayData["weather"][0]["description"].capitalize() + "*"

            day_descriptions.append(temp)

        index = 0
        
        # Send initial message (first day)
        embedVar = discord.Embed(title = "Weather for " + message.content[7:], color = 0xad0808)

        embedVar.add_field(name = day_descriptions[index]["name"], value = day_descriptions[index]["value"], inline = False)
        embedVar.set_thumbnail(url="https://openweathermap.org/img/wn/" + day_descriptions[index]["icon"] + "@2x.png")
        embedVar.set_footer(text=str(data["lat"]) + ", " + str(data["lon"]))

        msg = await message.channel.send(embed = embedVar)

        await msg.add_reaction("➡️")
    
        # Check for reactions added
        def check(reaction, user):
            return user == message.author and (str(reaction.emoji) == "➡️" or str(reaction.emoji) == "⬅️")

        # Event handler for adding reactions
        while True:
            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=15.0, check=check)
        
                await msg.remove_reaction("⬅️", user)
                await msg.remove_reaction("➡️", user)

                if str(reaction.emoji) == "➡️":
                    index += 1

                    # Reposition arrows at index 1
                    if index == 1:
                        await msg.remove_reaction("➡️", self.bot.user)
                        await msg.add_reaction("⬅️")
                        await msg.add_reaction("➡️")

                    # Remove option to skip forward at end of list
                    elif index == len(day_descriptions) - 1:
                        await msg.remove_reaction("➡️", self.bot.user)

                
                elif str(reaction.emoji) == "⬅️":
                    index -= 1

                    # Remove back arrow at index 0
                    if index == 0:
                        await msg.remove_reaction("⬅️", self.bot.user)
                    
                    # Add forward arrow at second to last index
                    elif index == len(day_descriptions) - 2:
                        await msg.add_reaction("➡️")
                    
                
                # Edit the message with the new day
                embedVar = discord.Embed(title = "Weather for " + message.content[7:], color = 0xad0808)

                embedVar.add_field(name = day_descriptions[index]["name"], value = day_descriptions[index]["value"], inline = False)

                embedVar.set_thumbnail(url="https://openweathermap.org/img/wn/" + day_descriptions[index]["icon"] + "@2x.png")

                embedVar.set_footer(text=str(data["lat"]) + ", " + str(data["lon"]))
                await msg.edit(embed = embedVar)
            except asyncio.TimeoutError:
                # Timeout
                try:
                    await msg.remove_reaction("⬅️", self.bot.user)
                    await msg.remove_reaction("➡️", self.bot.user)
                except:
                    pass
                break
def setup(bot):
    bot.add_cog(FCast(bot))