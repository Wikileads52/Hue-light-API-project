import requests
import os
import urllib3 #this import is optional 
from dotenv import load_dotenv
from app.url_type_selection import url_selection_function
from app.OpenWeatherMap_API_functions import weather_controller, open_user_settings_json
import bisect
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

load_dotenv()

#env variable
Bridge_IP = os.getenv("Hue_Bridge_IP")
UserName = os.getenv("Hue_UserName")

#header
headers= {
    "hue-application-key": UserName,
    "Content-Type": "application/json"
}


def define_color(url):
    color_options = {
        "1": "White",
        "2": "Red",
        "3": "Green",
        "4": "Blue",
        "5": "Yellow",
        "6": "Orange",
        "7": "Purple"
    }
    color_list = "\n".join(f"{k}: {v}" for k, v in color_options.items())
    color_selected = input(f"Select a color from the list: \n{color_list}\n> ")
    if color_selected in color_options:
        color_choice = color_options[color_selected]
        color_values = {
            "White": {"x": 0.3143, "y": 0.3301},
            "Red": {"x": 0.730, "y": 0.260},
            "Green": {"x": 0.120, "y": 0.820},
            "Blue": {"x": 0.080, "y": 0.200},
            "Yellow": {"x": 0.510, "y": 0.420},
            "Orange": {"x": 0.600, "y": 0.350},
            "Purple": {"x": 0.330, "y": 0.050}
        }
        body= { "color":{
            "xy": {
                "x": color_values[color_choice]["x"],
                "y": color_values[color_choice]["y"]
            }
        }}
        response = requests.put(url, headers=headers, json=body, timeout=5, verify=False)
        if response.status_code == 200:
            print(f"You chose {color_choice}")
        else:
            print(f"Failed to change color", response.status_code, response.text)
    else:
        print("Invalid selection. Please choose a valid option.")

weather_color_map = [
    (300, "Red", "Thunderstorm", 0.730, 0.260),
    (400, "Yellow", "Drizzle", 0.510, 0.420),
    (500, "White", "ErrorCode", 0.3143, 0.330),
    (600, "Orange", "Rain", 0.600, 0.350),
    (700, "Purple", "Snow", 0.330, 0.050),
    (800, "Green", "Atmosphere", 0.120, 0.820),
    (801, "Blue", "Clear", 0.080, 0.200),
    (804, "Green", "Cloudy", 0.120, 0.820),
    (float("inf"), "White", "OutOfBound", 0.3143, 0.330)
]

def color_weather(weather_color_map):
    data = weather_controller(settings)
    weather_code = data["cod"]
    print(type(weather_code))
    tresholds = [entry[0] for entry in weather_color_map]
    #print(tresholds)
    index = bisect.bisect_right(tresholds, weather_code -1)
    _, _, _, color_x, color_y = weather_color_map[index]
    #print(index)
    return color_x, color_y


def display_weather_color(url, color_x, color_y):
    try:
        body= { "color":{
            "xy":{
                "x": color_x, "y": color_y }
            }
        }
        response = requests.put(url, headers = headers, json = body, timeout=5, verify=False)
        if response.status_code == 200:
            print("Request successful")
            time.sleep(10)
            body= {"color":{
                "xy":{
                    "x": 0.3143, "y": 0.3301
                }
            }}
            resp = requests.put(url, headers = headers, json = body, timeout = 5, verify=False)
            if resp.status_code == 200:
                print("End displaying weather color")
            else:
                print(f"The request was not successful because of {resp.status_code}")
        else:
            print("Response was not 200; it was instead", response.status_code, response.text)
    except (ValueError, TypeError, ImportError, ConnectionError) as e:
        print(f"The color could not be displayed because of the following error ({e})")

#url = "https://192.168.1.106/clip/v2/resource/grouped_light/a0e7eb6a-19b5-472d-924e-7acefa7ee950"

if __name__ == "__main__":
    url = url_selection_function()
    #define_color(url)
    settings = open_user_settings_json()
    color_x, color_y = color_weather(weather_color_map)
    display_weather_color(url, color_x, color_y )