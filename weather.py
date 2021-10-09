import requests

class Weather():
    def __init__(self, API_KEY):
        self.API_KEY = API_KEY

    def getRawDataFromCity(self, city_name):
        base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&units=imperial&appid={self.API_KEY}"
        res = requests.get(base_url).json()

        if res["cod"] != 200:
            return None

        return res

    def getRawDataFromZip(self, zip_code):    
        base_url = f"http://api.openweathermap.org/data/2.5/weather?zip={zip_code}&units=imperial&appid={self.API_KEY}"
        res = requests.get(base_url).json()
        if res["cod"] != 200:
            return None

        return res

    def getRawDataFromCoords(self, coordinates):
        lat = coordinates[0]
        lon = coordinates[1]
        base_url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=imperial&appid={self.API_KEY}"
        res = requests.get(base_url).json()
        if res["cod"] != 200:
            return None

        return res

    def getSimpleWeather(self, location):
        # Coordinates
        if type(location) == list:
            data = self.getRawDataFromCoords(location)
        # Zip Code
        elif location.isnumeric():
            data = self.getRawDataFromZip(location)
        # City Name
        else:
            data = self.getRawDataFromCity(location)

        if data == None:
            return None

        return data

    def getRawForecastFromCoords(self, lat, lon):
        base_url = f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&units=imperial&appid={self.API_KEY}"
        res = requests.get(base_url).json()
        if "cod" in res:
            print("Error code " + str(res["cod"]))
            return None

        return res

    def getForecast(self, location):
        # Coordinates
        if type(location) == list:
            lat = location[0]
            lon = location[1]

        # Zip code
        elif location.isnumeric():
            tempData = self.getRawDataFromZip(location)
            lat = tempData["coord"]["lat"]
            lon = tempData["coord"]["lon"]

        # City name
        else:
            tempData = self.getRawDataFromCity(location)
            lat = tempData["coord"]["lat"]
            lon = tempData["coord"]["lon"]

        data = self.getRawForecastFromCoords(lat, lon)

        return data