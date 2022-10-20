import discord
from discord.ext import commands


class WeatherCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(description="Sends the bot's latency.")
    async def ping(self, ctx):
        await ctx.respond(f"Pong! Latency is {self.bot.latency}")


def setup(bot):
    bot.add_cog(WeatherCommand(bot))
