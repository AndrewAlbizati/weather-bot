import requests

class Weather():
    def __init__(self, API_KEY):
        self.API_KEY = API_KEY

    def getRawDataFromCity(self, city_name):
        base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={self.API_KEY}"
        res = requests.get(base_url).json()

        if res["cod"] != 200:
            return None

        return res

    def getRawDataFromZip(self, zip_code):    
        base_url = f"http://api.openweathermap.org/data/2.5/weather?zip={zip_code}&appid={self.API_KEY}"
        res = requests.get(base_url).json()
        if res["cod"] != 200:
            return None

        return res

    def getRawDataFromCoords(self, coordinates):
        lat = coordinates[0]
        lon = coordinates[1]
        base_url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={self.API_KEY}"
        res = requests.get(base_url).json()
        if res["cod"] != 200:
            return None

        return res

    def getWeather(self, location):
        if type(location) == int:
            data = self.getRawDataFromZip(location)
        elif type(location) == list:
            data = self.getRawDataFromCoords(location)
        else:
            data = self.getRawDataFromCity(location)

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