import os
import requests
import logging

class Ambient:
    def __init__(self):
        logging.info("Loading Ambient Weather provider")
        self.api_key = os.environ["AMBIENT_API_KEY"]
        self.app_key = os.environ["AMBIENT_APP_KEY"]
        self.device_mac = os.environ["AMBIENT_DEVICE_MAC"]
        self.zip_code = os.environ["WEATHER_ZIP_CODE"]

        self.endpoint = "https://api.ambientweather.net/v1/devices/"

    def _get(self):
        params = (
            ('applicationKey', self.app_key),
            ('apiKey', self.api_key),
        )
        response = requests.get(f'{self.endpoint}{self.device_mac}', params = params)
        return response.json()

    # Get the current weather conditions from Ambient Weather device
    def get_weather(self):
        d = self._get()[0]
        w = {}
        w['zip_code'] = self.zip_code
        w['temp'] = d['tempf']
        w['pressure'] = d['baromrelin']
        w['humidity'] = d['humidity']
        return w

    def sample_data_weather(self):
        w = [{
                "dateutc": 1612332600000,
                "humidityin": 46,
                "baromrelin": 29.33,
                "tempf": 37.6,
                "humidity": 99
        }]
        return w
