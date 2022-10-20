from discord.ext import commands


class Bot(commands.Bot):
    def __init__(self, weather_api_key, **options):
        super().__init__(**options)
        self.weather_api_key = weather_api_key

    async def on_ready(self):
        print(f'Logged on as {self.user}!')
