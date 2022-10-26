class Weather():
    def __init__(self, weather_data, forecast_data):
        self.weather_data = weather_data
        self.forecast_data = forecast_data

        if self.weather_data is not None and self.forecast_data is not None:
            self.lon = self.weather_data["coord"]["lon"]
            self.lat = self.weather_data["coord"]["lat"]

            self.timestamp = self.weather_data["dt"]
            self.city_name = self.weather_data["name"]
            self.weather_description = self.weather_data["weather"][0]["description"]

            self.temperature = self.weather_data["main"]["temp"]
            self.low_temperature = self.weather_data["main"]["temp_min"]
            self.high_temperature = self.weather_data["main"]["temp_max"]

            self.humidity = self.weather_data["main"]["humidity"]

    def get_daily_forecast(self, day_index):
        new_weather = Weather(None, self.forecast_data)
        new_weather.lon = self.lon
        new_weather.lat = self.lat

        new_weather.timestamp = self.forecast_data["daily"][day_index]["dt"]
        new_weather.city_name = self.city_name
        new_weather.weather_description = self.forecast_data["daily"][day_index]["weather"][0]["description"]

        new_weather.temperature = self.forecast_data["daily"][day_index]["temp"]["day"]
        new_weather.low_temperature = self.forecast_data["daily"][day_index]["temp"]["min"]
        new_weather.high_temperature = self.forecast_data["daily"][day_index]["temp"]["max"]

        new_weather.humidity = self.forecast_data["daily"][day_index]["humidity"]

        return new_weather
