import requests
import os
import urllib3 #this import is optional 
from dotenv import load_dotenv
from app.url_type_selection import url_selection_function

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
            print("Failed to change color", response.status_code, response.text)
    else:
        print("Invalid selection. Please choose a valid option.")

def color_weather():



        url = url_selection_function()
        define_color(url)