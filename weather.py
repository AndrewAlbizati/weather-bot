import requests

class Weather():
    def __init__(self, API_KEY):
        self.API_KEY = API_KEY

    def getSimpleRawDataFromCity(self, city_name):
        base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={self.API_KEY}"
        res = requests.get(base_url).json()

        if res["cod"] != 200:
            return None

        return res

    def getSimpleRawDataFromZip(self, zip_code):    
        base_url = f"http://api.openweathermap.org/data/2.5/weather?zip={zip_code}&appid={self.API_KEY}"
        res = requests.get(base_url).json()
        if res["cod"] != 200:
            return None

        return res

    def getSimpleRawDataFromCoords(self, coordinates):
        lat = coordinates[0]
        lon = coordinates[1]
        base_url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={self.API_KEY}"
        res = requests.get(base_url).json()
        if res["cod"] != 200:
            return None

        return res

    def getSimpleWeather(self, location):
        if type(location) == list:
            data = self.getSimpleRawDataFromCoords(location)
        elif location.isnumeric():
            data = self.getSimpleRawDataFromZip(location)
        else:
            data = self.getSimpleRawDataFromCity(location)

        if data == None:
            return None
        
        weatherDict = {}

        weatherDict["temperature"] = float(round(float((data["main"]["temp"] - 273.15) * 1.8 + 32), 2))
        weatherDict["description"] = str(data["weather"][0]["description"])

        weatherDict["humidity"] = int(data["main"]["humidity"])
        weatherDict["pressure"] = int(data["main"]["pressure"])

        weatherDict["windspeed"] = float(data["wind"]["speed"])
        weatherDict["winddir"] = int(data["wind"]["deg"])

        weatherDict["sunrise"] = data["sys"]["sunrise"]
        weatherDict["sunset"] = data["sys"]["sunset"]

        return weatherDict

    def getAdvancedRawDataFromCoords(self, lat, lon):
        base_url = f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&units=imperial&appid={self.API_KEY}"
        res = requests.get(base_url).json()
        if "cod" in res:
            print("Error code " + str(res["cod"]))
            return None

        return res

    def getAdvancedWeather(self, location):
        # Coordinates
        if type(location) == list:
            lat = location[0]
            lon = location[1]

        # Zip code
        elif location.isnumeric():
            tempData = self.getSimpleRawDataFromZip(location)
            lat = tempData["coord"]["lat"]
            lon = tempData["coord"]["lon"]

        # City name
        else:
            tempData = self.getSimpleRawDataFromCity(location)
            lat = tempData["coord"]["lat"]
            lon = tempData["coord"]["lon"]

        data = self.getAdvancedRawDataFromCoords(lat, lon)

        return data