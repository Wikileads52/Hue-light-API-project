import os
from dotenv import load_dotenv
import app.get_url as get_url


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

    #Implementation of the selection logic
    type_selected = (input(f"Select from the list which type of element you want to change: \n{type_needed_list}\n> "))
    if type_selected =="1":
        print(f"You selected Room: ")
        url_group_type_selected = "grouped_light"
        selected_rooms = get_url.url_room_selection()
        #print(selected_rooms)
        url = selected_rooms
    elif type_selected =="2":
        print(f"You selected Zone: ")
        url_group_type_selected = "grouped_light"
        selected_zones = get_url.url_zone_selection()
        #print(selected_zones)
        url = selected_zones
    elif type_selected =="3":
        url_group_type_selected = "light"
        selected_lights = get_url.url_light_selection()
        #print(selected_lights)
        url = selected_lights
    elif type_selected =="4":
        print("Exiting the application")
        exit()
        return None
    else:
        print("Invalid entry")
        url_selection_function()
        return None
    return url

#execution bloc
if __name__ == "__main__":
   while True:
    url = url_selection_function()
