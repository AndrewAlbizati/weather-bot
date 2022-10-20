import requests


class WeatherFunctions():
    def __init__(self, api_key):
        self.API_KEY = api_key

    def get_raw_data_from_city(self, city_name):
        base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&units=imperial&appid={self.API_KEY}"
        res = requests.get(base_url).json()

        if res["cod"] != 200:
            return None

        return res

    def get_raw_data_from_zip(self, zip_code):
        base_url = f"http://api.openweathermap.org/data/2.5/weather?zip={zip_code}&units=imperial&appid={self.API_KEY}"
        res = requests.get(base_url).json()
        if res["cod"] != 200:
            return None

        return res

    def get_raw_data_from_coords(self, coordinates):
        lat = coordinates[0]
        lon = coordinates[1]
        base_url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=imperial&appid={self.API_KEY}"
        res = requests.get(base_url).json()
        if res["cod"] != 200:
            return None

        return res

    def get_simple_weather(self, location):
        # Coordinates
        if type(location) == list:
            data = self.get_raw_data_from_coords(location)
        # Zip Code
        elif location.isnumeric():
            data = self.get_raw_data_from_zip(location)
        # City Name
        else:
            data = self.get_raw_data_from_city(location)

        if data == None:
            return None

        return data

    def get_raw_forecast_from_coords(self, lat, lon):
        base_url = f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&units=imperial&appid={self.API_KEY}"
        res = requests.get(base_url).json()
        if "cod" in res:
            print("Error code " + str(res["cod"]))
            return None

        return res

    def get_forecast(self, location):
        # Coordinates
        if type(location) == list:
            lat = location[0]
            lon = location[1]

        # Zip code
        elif location.isnumeric():
            tempData = self.get_raw_data_from_zip(location)
            lat = tempData["coord"]["lat"]
            lon = tempData["coord"]["lon"]

        # City name
        else:
            tempData = self.get_raw_data_from_city(location)
            lat = tempData["coord"]["lat"]
            lon = tempData["coord"]["lon"]

        data = self.get_raw_data_from_coords((lat, lon))

        return data