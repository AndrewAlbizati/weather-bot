from discord.ext import commands
import discord
from discord import Option

import asyncio
from weather_utils import Weather_Utils
import json
from datetime import datetime

if __name__ == "__main__":
    with open("tokens.json", "r") as f:
        data = json.load(f)

    TOKEN = data["discord"]
    WEATHER_API_KEY = data["weather"]
    
    bot = commands.Bot()
    weather_utils = Weather_Utils(WEATHER_API_KEY)

    @bot.event
    async def on_ready():
        print(f'{bot.user} has connected to Discord!')

    @bot.slash_command(description="Returns the weather for a city/state")
    async def weather(ctx, location: Option(str, "Location that the weather will be found for", required=True, default=None)):
        if location == None:
            return        

        try:
            # Correct if user sent coordinates
            if len(location.replace(", ", ",").split(",")) == 2:
                location = location.replace(", ", ",")
    
                lat = float(location.split(",")[0])
                lon = float(location.split(",")[1])

                data = weather_utils.getSimpleWeather([lat, lon])      
            else:
                data = weather_utils.getSimpleWeather(location)
        except:
            await ctx.respond("Location not found!")
            return
        
        # Location not found
        if data == None:
            await ctx.respond("Location not found.")
            return
        
        # Find local time for location
        timestamp = datetime.utcfromtimestamp(data["dt"] + data["timezone"])
        date = timestamp.strftime("%I:%M:%S %p") # HH:MM:SS AM/PM
        
        # Create embed
        embedVar = discord.Embed(title = "Weather for " + " ".join([word.capitalize() for word in location.split(" ")]) + " (" + date + " local time)", color = 0xad0808)
        embedVar.description = str(
        "Temp: **" + str(data["main"]["temp"]) + "** (" + str(data["main"]["temp_min"]) + " - " + str(data["main"]["temp_max"]) + ")\n"
        "Hum: **" + str(data["main"]["humidity"]) + "%**\n"
        "*" + str(data["weather"][0]["description"]).capitalize() + "*")
        
        embedVar.set_thumbnail(url="https://openweathermap.org/img/wn/" + data["weather"][0]["icon"] + "@2x.png")
        embedVar.set_footer(text=str(data["coord"]["lat"]) + ", " + str(data["coord"]["lon"]))

        await ctx.respond(embed = embedVar)


    @bot.slash_command(description="Location that the forecast will be found for")
    async def forecast(ctx, location: Option(str, "Location", required=True, default=None)):
        if location == None:
            return
        
        initial_message = await ctx.respond("Collecting data...")

        try:
            # Correct if user sent coordinates
            if len(location.replace(", ", ",").split(",")) == 2:
                location = location.replace(", ", ",")
    
                lat = float(location.split(",")[0])
                lon = float(location.split(",")[1])

                data = weather_utils.getForecast([lat, lon])      
            else:
                data = weather_utils.getForecast(location)
        except:
            await initial_message.delete_original_message()
            await ctx.channel.send("Location not found!")
            return


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
        embedVar = discord.Embed(title = "Forecast for " + " ".join([word.capitalize() for word in location.split(" ")]), color = 0xad0808)

        embedVar.add_field(name = day_descriptions[index]["name"], value = day_descriptions[index]["value"], inline = False)
        embedVar.set_thumbnail(url="https://openweathermap.org/img/wn/" + day_descriptions[index]["icon"] + "@2x.png")
        embedVar.set_footer(text=str(data["lat"]) + ", " + str(data["lon"]))

        await initial_message.delete_original_message()
        msg = await ctx.channel.send(embed = embedVar)

        await msg.add_reaction("➡️")
    
        # Check for reactions added
        def check(reaction, user):
            return user == ctx.author and (str(reaction.emoji) == "➡️" or str(reaction.emoji) == "⬅️")

        # Event handler for adding reactions
        while True:
            try:
                reaction, user = await bot.wait_for('reaction_add', timeout=15.0, check=check)
        
                await msg.remove_reaction("⬅️", user)
                await msg.remove_reaction("➡️", user)

                if str(reaction.emoji) == "➡️":
                    index += 1

                    # Reposition arrows at index 1
                    if index == 1:
                        await msg.remove_reaction("➡️", bot.user)
                        await msg.add_reaction("⬅️")
                        await msg.add_reaction("➡️")

                    # Remove option to skip forward at end of list
                    elif index == len(day_descriptions) - 1:
                        await msg.remove_reaction("➡️", bot.user)

                
                elif str(reaction.emoji) == "⬅️":
                    index -= 1

                    # Remove back arrow at index 0
                    if index == 0:
                        await msg.remove_reaction("⬅️", bot.user)
                    
                    # Add forward arrow at second to last index
                    elif index == len(day_descriptions) - 2:
                        await msg.add_reaction("➡️")
                    
                
                # Edit the message with the new day
                embedVar = discord.Embed(title = "Forecast for " + " ".join([word.capitalize() for word in location.split(" ")]), color = 0xad0808)

                embedVar.add_field(name = day_descriptions[index]["name"], value = day_descriptions[index]["value"], inline = False)

                embedVar.set_thumbnail(url="https://openweathermap.org/img/wn/" + day_descriptions[index]["icon"] + "@2x.png")

                embedVar.set_footer(text=str(data["lat"]) + ", " + str(data["lon"]))
                await msg.edit(embed = embedVar)
            except asyncio.TimeoutError:
                # Timeout
                try:
                    await msg.remove_reaction("⬅️", bot.user)
                    await msg.remove_reaction("➡️", bot.user)
                except:
                    pass
                break


    bot.run(TOKEN)