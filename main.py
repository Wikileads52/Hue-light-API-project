import requests
import json
import os
from time import sleep
from dotenv import load_dotenv
from url_type_selection import url_selection_function


load_dotenv()

#env variable
Bridge_IP = os.getenv("Hue_Bridge_IP")
UserName = os.getenv("Hue_UserName")
Certificate_Path = os.getenv("Certificate_Path")

#Header
headers= {
    "hue-application-key": UserName,
    "Content-Type": "application/json"
}

def check_light_status():
    response = requests.get(url, headers=headers, timeout=5, verify= False)
    if response.status_code == 200:
        data = response.json()
        on_off = data["data"][0]["on"]["on"]
        print(f"Call is a success, The light was: {'On' if on_off else 'Off'}")
        return on_off 
    else:
        print("Call is a failure", response.status_code, response.text)



def user_select_what_to_do(on_off):
    actions_available={
        "1" : "Turn light on/off",
        "2" : "Choose brightness",
        "3" : "Exit"}
    if on_off:
        actions_list = "\n".join(f"{k}: {v}" for k, v in actions_available.items())
        actions_selected = (input(f"Select from list of actions what you want to do : \n{actions_list}\n> "))
        if actions_selected == "1":
            print("You chose to switch the light off")
            new_light_state = turn_light_on_off(on_off)
        elif actions_selected == "2":
            print ("You chose to change brightness")
            define_brightness()
            return on_off
        else:
            print("You chose to quit the program")
            return None, None
    else:
        new_light_state = turn_light_on_off(on_off)
        return new_light_state

def turn_light_on_off(on_off):
    if on_off:
        body={"on":{"on": False}}
    else:
        body={"on":{"on": True}}
    response = requests.put(url, headers=headers, json=body, timeout=5, verify= False)
    if response.status_code == 200:
        response = requests.get(url, headers=headers, timeout=5, verify= False)
        data = response.json()
        new_light_state = data["data"][0]["on"]["on"]
        print(f"The light is now: {'On' if new_light_state else 'Off'}")
        print(f"Call is a success")
        return new_light_state
    else:
        print("Call is a failure", response.status_code, response.text)

# new_light_state = turn_light_on_off(on_off)

def define_brightness():
    try:
        select_dimming = int(input("Set light dimming between 0 to 100: ").strip())
        if 0 < select_dimming <= 100:
            body = {"dimming":{"brightness": select_dimming}}
            response = requests.put(url, headers=headers, json=body, timeout=5, verify= False)
            print (f"The brightness is now set at: {select_dimming}")
            data = response.json()
        else:
            print("Input a valid number")
            return None, None
    except ValueError:
        print("input a correct number")
        define_brightness()
        return None, None
while True:            
    if __name__ == "__main__":
        url = url_selection_function()
        on_off= check_light_status()
        user_select_what_to_do(on_off)

