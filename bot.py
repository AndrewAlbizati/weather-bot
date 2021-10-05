import discord
from weather import Weather

if __name__ == "__main__":
    with open("tokens.txt", "r") as f:
        lines = f.readlines()
        lines = [line.rstrip() for line in lines]

        TOKEN = lines[0]
        API_KEY = lines[1]
    

    client = discord.Client()
    weather = Weather(API_KEY)

    @client.event
    async def on_ready():
        print(f'{client.user} has connected to Discord!')
    

    @client.event
    async def on_message(message):
        if message.author.bot:
            return
        
        if message.content.lower() == "!weather":
            pass
            

    client.run(TOKEN)