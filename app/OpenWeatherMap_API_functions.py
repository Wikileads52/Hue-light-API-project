import requests
import os
import json
import time
import urllib3 #this import is optional 
from dotenv import load_dotenv

load_dotenv()
OpenWeather_API_Key = os.getenv("OpenWeather_API_Key")


Paris_coordinates : dict={
    "lat" : 48.866667,
    "lon" : 2.33333
}


def get_weather_now():
    weather_url :str = f"https://api.openweathermap.org/data/2.5/weather?lat={Paris_coordinates['lat']}&lon={Paris_coordinates['lon']}&units=metric&appid={OpenWeather_API_Key}"
    response= requests.get(weather_url)
    if response.status_code ==200:
        data : str = response.json()
        parsed :dict =(json.dumps(data, indent=4))
        #print(parsed)
        return data, parsed
    else:
        print(f"call failed", response.status_code, response.text)
        return None

data, parsed = get_weather_now()


def display_present_weather_data(data):
    weather_data : dict ={
        "main" : data["weather"][0]["description"],
        "description" : data["weather"][0]["description"],
        "actual_temp" : data["main"]["temp"],
        "temp_min" : data["main"]["temp_min"],
        "temp_max" : data["main"]["temp_max"]
    }
    print(f"The weather in Paris is currently {weather_data["description"]}, "
        f"with current temperature being {weather_data["actual_temp"]}°C. "
        f"Today, temperature minimum is {weather_data["temp_min"]}°C, and maximum is {weather_data["temp_max"]}°C.")

def color_selection(weather_url):
    weather_url :str = f"https://api.openweathermap.org/data/2.5/weather?lat={Paris_coordinates['lat']}&lon={Paris_coordinates['lon']}&units=metric&appid={OpenWeather_API_Key}"
    

if __name__ == "__main__":
    while True:
        display_present_weather_data(data)