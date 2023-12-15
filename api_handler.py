# api_handler.py
import requests
class ApiHandler:
    def __init__(self, openweathermap_api_key, opencage_api_key):
        self.openweathermap_api_key = "ee9e8dc99954f000e07a583dfd152412"
        self.opencage_api_key = "b8cd8b7ad6cd4435b414a0dc4d742d09"

    def get_openweathermap_data(self, latitude, longitude, start_time, end_time):
        openweathermap_url = "https://api.openweathermap.org/data/2.5/"
        params = {
            'lat': latitude,
            'lon': longitude,
            'start': start_time,  # Start time in Unix timestamp
            'end': end_time,  # End time in Unix timestamp
            'appid': self.openweathermap_api_key,
        }

        response = requests.get(openweathermap_url, params=params)
        data = response.json()

        return data
    def get_geocoding_data(self, project_location):
        opencage_url = "https://api.opencagedata.com/geocode/v1/json"

        # Parameters for geocoding
        params = {
            'q': project_location,
            'key': self.opencage_api_key,
        }

        # Make the API request
        response = requests.get(opencage_url, params=params)
        data = response.json()

        return data