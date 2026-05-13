import requests
import os
import json
import time
import urllib3 #this import is optional 
from dotenv import load_dotenv
import json
from pathlib import Path


load_dotenv()
OpenWeather_API_Key = os.getenv("OpenWeather_API_Key")


Paris_coordinates : dict={
    "lat" : 48.866667,
    "lon" : 2.33333
}
def open_user_settings_json():
    try:
        settings_path = Path(__file__).resolve().parent.parent / "Utils" / "user_settings.json"
        with open(settings_path, "r") as user_settings:
            settings = json.load(user_settings)
            print(f"API configured to refresh every {settings["weather_map_settings"]["wheather_map_update_interval"]} minutes")
            return settings

    except (FileNotFoundError, json.JSONDecodeError) as  e:
        print(f"Encountered an error reading the settings file ({e})")

def get_weather_now(settings):
    lat = settings["weather_map_settings"]["weather_prefered_location_coordinates"]["lat"]
    lon = settings["weather_map_settings"]["weather_prefered_location_coordinates"]["lon"]
    mesure_system= settings["weather_map_settings"]["weather_prefered_units"]
    print(type(mesure_system))
    print(mesure_system)
    weather_url :str = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units={mesure_system}&appid={OpenWeather_API_Key}"
    response= requests.get(weather_url)
    if response.status_code ==200:
        data : str = response.json()
        parsed :dict =(json.dumps(data, indent=4))
        #print(parsed)
        return data, parsed
    else:
        print(f"call failed", response.status_code, response.text)
        return None, response.status_code


def weather_controller(settings):
    result = get_weather_now(settings)
    #print(type(result))
    if result is not None :
        data, parsed = result
        #print(type(data))
        print(f"The request succeded with code:{data["cod"]}")
        return data
    else:
        print(f"The request to WeatherMap failed")
        return None


def display_present_weather_data(data):
    weather_data : dict ={
        "main" : data["weather"][0]["description"],
        "weather_id": data["weather"][0]["id"],
        "description" : data["weather"][0]["description"],
        "actual_temp" : data["main"]["temp"],
        "temp_min" : data["main"]["temp_min"],
        "temp_max" : data["main"]["temp_max"]
    }
    print(f"The weather in Paris is currently {weather_data["description"]}, "
        f"with current temperature being {weather_data["actual_temp"]}°C. "
        f"Today, temperature minimum is {weather_data["temp_min"]}°C, and maximum is {weather_data["temp_max"]}°C."
        f"weather id is {weather_data["weather_id"]}")


def auto_refresh_weather_info(data, timeout : int):
    time_in_seconds = timeout * 60
    try:    
        while True:
            if data is not None:
                weather_data , parsed = data
                display_present_weather_data(weather_data)
                time.sleep(time_in_seconds)
            else :
                print(f"The request failed, the next update will be in {timeout}")
                return None
    except KeyboardInterrupt:
            print("The user stopped the auto-refresh")

if __name__ == "__main__":
    #while True:
        settings = open_user_settings_json()
        #get_weather_now(settings)
        data = weather_controller(settings)
        display_present_weather_data(data)
        #auto_refresh_weather_info(data, settings["weather_map_settings"]["wheather_map_update_interval"])