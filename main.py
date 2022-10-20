import discord.errors
import requests
import bot
import os
import json


def main():
    api_key = get_token("weather")
    while not test_weather_key(api_key):
        reset_key("weather")
        api_key = get_token("weather")

    b = bot.Bot(api_key)

    for file in os.listdir("./cogs"):
        if file.endswith(".py"):
            extension = f"cogs.{file[0:-3]}"

            try:
                b.load_extension(extension)
                print(f"Loaded {extension}")
            except Exception as e:
                exc = '{}: {}'.format(type(e).__name__, e)
                print('Failed to load extension {}\n{}'.format(extension, exc))

    discord_token = get_token("discord")
    try:
        b.run(discord_token)
    except discord.errors.LoginFailure as e:
        print(e)
        reset_key("discord")
        assign_token("discord")
        print("Please run the program again")


def create_tokens_file():
    with open("tokens.json", "w") as f:
        f.write("{\n\t\"discord\": \"\",\n\t\"weather\": \"\"\n}")


def get_token(token_name):
    if "tokens.json" not in os.listdir("."):
        create_tokens_file()
        token = assign_token(token_name)

        return token
    else:
        with open("tokens.json", "r") as f:
            data = json.load(f)

        if token_name in data:
            return data[token_name]
        else:
            token = assign_token(token_name)
            return token


def assign_token(token_name):
    token = input(f"Paste {token_name} key: ")

    with open("tokens.json", "r") as f:
        tokens_data = json.load(f)

    tokens_data[token_name] = token

    with open("tokens.json", "w") as f:
        json.dump(tokens_data, f, indent=4)

    return token


def test_weather_key(api_key):
    url = f"http://api.openweathermap.org/data/2.5/weather?q=San Diego&units=imperial&appid={api_key}"
    res = requests.get(url).json()

    return res["cod"] == 200


def reset_key(token_name):
    if "tokens.json" in os.listdir("."):
        with open("tokens.json", "r") as f:
            tokens_data = json.load(f)

        try:
            del tokens_data[token_name]
        except KeyError:
            pass

        with open("tokens.json", "w") as f:
            json.dump(tokens_data, f, indent=4)


if __name__ == "__main__":
    main()
