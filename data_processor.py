
# data_processor.py

class DataProcessor:
    def __init__(self, openweathermap_data, geocoding_data):
        self.openweathermap_data = openweathermap_data
        self.geocoding_data = geocoding_data

    def process_all_data(self):
        openweathermap_processed_data = self.process_openweathermap_data()
        geocoding_processed_data = self.process_geocoding_data()
        additional_analysis_result = self.perform_additional_analysis(openweathermap_processed_data)

        return {
            'openweathermap_processed_data': openweathermap_processed_data,
            'geocoding_processed_data': geocoding_processed_data,
            'additional_analysis_result': additional_analysis_result,
            'result_message': self.generate_result_message(additional_analysis_result)
        }

    def perform_additional_analysis(self, openweathermap_processed_data):
        sunny_days = sum(1 for day in openweathermap_processed_data if 'Clear' in day.get('weather_description', ''))

        total_days = len(openweathermap_processed_data)
        sunny_percentage = (sunny_days / total_days) * 100 if total_days > 0 else 0

        return {
            'sunny_days': sunny_days,
            'total_days': total_days,
            'sunny_percentage': sunny_percentage
        }

    def generate_result_message(self, additional_analysis_result):
        sunny_percentage = additional_analysis_result.get('sunny_percentage', 0)

        if 70 <= sunny_percentage <= 100:
            return "Good weather, good luck"
        elif 50 <= sunny_percentage < 70:
            return "Looks good, hope everything goes well"
        elif 30 <= sunny_percentage < 50:
            return "I am a little concerned about your safety, I hope you will think about it"
        else:
            return "We don't recommend you start building at this time of the year, you can do it at another time"

    def process_openweathermap_data(self):
        processed_data = []
        latitude = self.openweathermap_data.get('lat')
        longitude = self.openweathermap_data.get('lon')
        timezone = self.openweathermap_data.get('timezone')
        current_weather = self.openweathermap_data.get('current', {})
        current_temperature = current_weather.get('temp')
        current_humidity = current_weather.get('humidity')

        daily_forecast = self.openweathermap_data.get('daily', [])
        for day_forecast in daily_forecast:
            date = day_forecast.get('dt')
            temperature_day = day_forecast.get('temp', {}).get('day')
            temperature_night = day_forecast.get('temp', {}).get('night')
            humidity = day_forecast.get('humidity')
            weather_description = day_forecast.get('weather', [])[0].get('description')
            # Create a processed entry for each day's forecast
            processed_entry = {
                'date': date,
                'latitude': latitude,
                'longitude': longitude,
                'timezone': timezone,
                'temperature_day': temperature_day,
                'temperature_night': temperature_night,
                'humidity': humidity,
                'weather_description': weather_description
            }
            processed_data.append(processed_entry)

        return processed_data

    def process_geocoding_data(self):
        processed_data = []
        # Extract relevant information from the OpenCageData response
        results = self.geocoding_data.get('results', [])

        if results:
            result = results[0]
            formatted_address = result.get('formatted', '')
            latitude = result.get('geometry', {}).get('lat')
            longitude = result.get('geometry', {}).get('lng')
            confidence = result.get('confidence')
            annotations = result.get('annotations', {})
            timezone = annotations.get('timezone', {}).get('name')
            currency_info = annotations.get('currency', {})
            # Create a processed entry
            processed_entry = {
                'formatted_address': formatted_address,
                'latitude': latitude,
                'longitude': longitude,
                'confidence': confidence,
                'timezone': timezone,
                'currency_info': currency_info
            }
            processed_data.append(processed_entry)

        return processed_data
