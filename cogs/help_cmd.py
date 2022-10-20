import discord
from discord.ext import commands


class HelpCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(description="Sends information about the bot.")
    async def help(self, ctx):
        await ctx.respond("Help!")


def setup(bot):
    bot.add_cog(HelpCommand(bot))
