import requests
import json
import os
from time import sleep
from dotenv import load_dotenv
from get_room_url import url_room_selection
from get_zone_url import url_zone_selection
from get_light_url import url_light_selection

load_dotenv()

#env variable
Bridge_IP = os.getenv("Hue_Bridge_IP")
UserName = os.getenv("Hue_UserName")


#header
headers= {
    "hue-application-key": UserName,
    "Content-Type": "application/json"
}


#Url type group needed selection function
def url_selection_function():
    type_needed={
        "1":"Room",
        "2":"Zone",
        "3":"Single light",
        "4":"Exit the application"
    }
    type_needed_list = "\n".join(f"{k}: {v}" for k, v in type_needed.items())
    
    type_selected = (input(f"Select from the list which type of element you want to change: \n{type_needed_list}\n> "))
    if type_selected =="1":
        print(f"You selected Room: ")
        url_group_type_selected = "grouped_light"
        selected_rooms = url_room_selection()
        print(selected_rooms)
        url = selected_rooms
    elif type_selected =="2":
        print(f"You selected Zone: ")
        url_group_type_selected = "grouped_light"
        selected_zones = url_zone_selection()
        print(selected_zones)
        url = selected_zones
    elif type_selected =="3":
        url_group_type_selected = "light"
        selected_lights = url_light_selection()
        print(selected_lights)
        url = selected_lights
    elif type_selected =="4":
        print("Exiting the application")
        exit()
        return None
    else:
        print("Invalid entry")
        return None
    #return url_group_type_selected
    return url
#execution bloc

if __name__ == "__main__":
   url = url_selection_function()

#print(url)
#url = f"https://{Bridge_IP}/clip/v2/resource/{url_group_type_selected}/{grouped_light_id}"
#print(url)
