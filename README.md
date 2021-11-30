# Weather Bot
This Discord bot is designed to return weather data from OpenWeatherMap for a provided location. This bot runs on Python 3.10.0

## Setup
First, go to [the Discord developers page](https://discord.com/developers/docs/intro) and create an application, then register a bot. 
The bot will need the following permissions:

**OAuth2 scopes:**
- bot
- applications.commands

Copy the bot's token to your clipboard.

Next, add a file called `config.json` to the main folder and add the following:
```json
{
    "discord": "discord token goes here",
    "weather": "OpenWeatherMap api key goes here"
}
```

# Commands
- **/weather &lt;location>** *Returns the weather for a city/state*
- **/forecast &lt;location>** *Returns the forecast for a city/state*

## External Dependencies
- **Pycord** `pip install git+https://github.com/Pycord-Development/pycord`