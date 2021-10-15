from discord.ext import commands

startup_extensions = ["fcast", "weather"]

if __name__ == "__main__":
    # Get tokens from tokens.txt
    # First line = Discord
    # Second line = OpenWeatherMap
    with open("tokens.txt", "r") as f:
        lines = f.readlines()
        lines = [line.rstrip() for line in lines]

        TOKEN = lines[0]
    
    bot = commands.Bot(command_prefix = "!")

    @bot.event
    async def on_ready():
        print(f'{bot.user} has connected to Discord!')

    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))
    
    bot.run(TOKEN)