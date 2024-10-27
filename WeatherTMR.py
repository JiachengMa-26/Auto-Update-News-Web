import requests
from datetime import datetime, timedelta

class WeatherTMR:
    def __init__(self, api_key, zip_code, country_code):
        self.api_key = api_key
        self.zip_code = zip_code
        self.country_code = country_code
        self.api_url = f'http://api.openweathermap.org/data/2.5/forecast?zip={zip_code},{country_code}&appid={api_key}&units=metric'

    def celsius_to_fahrenheit(self, celsius):
        return celsius * 9/5 + 32

    def get_tomorrow_weather(self):
        response = requests.get(self.api_url)
        if response.status_code == 200:
            data = response.json()
            tomorrow = (datetime.now() + timedelta(days=1)).date()
            daily_forecasts = [forecast for forecast in data['list'] if datetime.fromtimestamp(forecast['dt']).date() == tomorrow]
            
            if daily_forecasts:
                weather_data = {
                    'min_temp_c': float('inf'),
                    'max_temp_c': float('-inf'),
                    'weather_description': daily_forecasts[0]['weather'][0]['description'],
                    'humidity': 0,
                    'wind_speed': 0,
                    'total_rain': 0.0,
                    'rain_times': [],
                    'max_wind_speed': float('-inf'),
                    'max_wind_speed_time': "",
                    'sunrise': None,
                    'sunset': None,
                    'daylight_duration': None,
                    'nighttime_duration': None
                }
                count = len(daily_forecasts)
                
                for forecast in daily_forecasts:
                    temp_min = forecast['main']['temp_min']
                    temp_max = forecast['main']['temp_max']
                    weather_data['humidity'] += forecast['main']['humidity']
                    wind_speed_current = forecast['wind']['speed']
                    rain = forecast.get('rain', {}).get('3h', 0.0)
                    weather_data['total_rain'] += rain
                    
                    forecast_time = datetime.fromtimestamp(forecast['dt']).strftime('%H:%M')

                    if rain > 0:
                        weather_data['rain_times'].append((forecast_time, rain))

                    if wind_speed_current > weather_data['max_wind_speed']:
                        weather_data['max_wind_speed'] = wind_speed_current
                        weather_data['max_wind_speed_time'] = forecast_time
                    
                    if temp_min < weather_data['min_temp_c']:
                        weather_data['min_temp_c'] = temp_min
                    if temp_max > weather_data['max_temp_c']:
                        weather_data['max_temp_c'] = temp_max
                    
                    if not weather_data['sunrise'] and not weather_data['sunset']:
                        city_data = data['city']
                        sunrise_timestamp = city_data['sunrise']
                        sunset_timestamp = city_data['sunset']
                        weather_data['sunrise'] = datetime.fromtimestamp(sunrise_timestamp).strftime('%H:%M:%S')
                        weather_data['sunset'] = datetime.fromtimestamp(sunset_timestamp).strftime('%H:%M:%S')

                        sunrise_dt = datetime.fromtimestamp(sunrise_timestamp)
                        sunset_dt = datetime.fromtimestamp(sunset_timestamp)
                        weather_data['daylight_duration'] = sunset_dt - sunrise_dt
                        weather_data['nighttime_duration'] = timedelta(hours=24) - weather_data['daylight_duration']

                weather_data['average_humidity'] = weather_data['humidity'] / count
                weather_data['min_temp_f'] = self.celsius_to_fahrenheit(weather_data['min_temp_c'])
                weather_data['max_temp_f'] = self.celsius_to_fahrenheit(weather_data['max_temp_c'])
                
                return weather_data
            else:
                raise ValueError("Tomorrow's data is not available, please try again later.")
        else:
            raise ConnectionError("Failed to retrieve weather information. Please check the API settings.")