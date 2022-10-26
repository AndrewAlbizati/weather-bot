import discord
from discord.ext import commands


class HelpCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.url = "https://github.com/AndrewAlbizati/weather-bot"

    @discord.slash_command(description="Sends information about the bot.")
    async def help(self, ctx):
        embed = discord.Embed()
        embed.title = "Help"
        embed.add_field(name="How to Use", value="Type `/weather <city>` in any channel to use this bot\n", inline=False)
        embed.add_field(name="More Information", value=f"Visit [here]({self.url}) for more information", inline=False)

        await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(HelpCommand(bot))
