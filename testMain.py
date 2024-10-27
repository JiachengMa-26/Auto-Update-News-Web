# main.py
from WeatherTMR import WeatherTMR
from datetime import datetime

def main():
    api_key = 'bcbbbe8045522445169c28a6b08b4758'
    zip_code = '11355'
    country_code = 'us'
    forecast = WeatherTMR(api_key, zip_code, country_code)
    
    try:
        weather_data = forecast.get_tomorrow_weather()
        print("明天的天气预报：")
        print(f"最低温度: {weather_data['min_temp_c']}°C / {weather_data['min_temp_f']}°F")
        print(f"最高温度: {weather_data['max_temp_c']}°C / {weather_data['max_temp_f']}°F")
        print(f"天气状况: {weather_data['weather_description']}")
        print(f"平均湿度: {weather_data['average_humidity']}%")
        print(f"总降雨量: {weather_data['total_rain']} mm")
        if weather_data['rain_times']:
            print("降雨时间段及降雨量:")
            for time, rain in weather_data['rain_times']:
                print(f"  时间: {time}, 降雨量: {rain} mm")
        else:
            print("未来24小时内无降雨预报。")
        print(f"最大风速: {weather_data['max_wind_speed']} 米/秒 (时间: {weather_data['max_wind_speed_time']})")
        print(f"日出时间: {weather_data['sunrise']}")
        print(f"日落时间: {weather_data['sunset']}")
        print(f"白昼时长: {weather_data['daylight_duration']}")
        print(f"夜晚时长: {weather_data['nighttime_duration']}")
    except (ValueError, ConnectionError) as e:
        print(e)

if __name__ == "__main__":
    main()