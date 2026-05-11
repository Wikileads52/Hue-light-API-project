import requests
import os
import urllib3
from dotenv import load_dotenv

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

def url_room_selection():
    name_rooms : list =[]
    rid_rooms : list =[]
    url = f"https://{Bridge_IP}/clip/v2/resource/room"
    response = requests.get(url, headers=headers, timeout=5, verify= False)
    if response.status_code == 200:
        data = response.json()
        for group in data["data"]:
            metadata_data = group['metadata']['name']
            name_rooms.append(metadata_data)
            for service in group["services"]:
                if service ["rtype"] == "grouped_light":
                    rid_rooms.append(service["rid"])
        for i, item in enumerate(name_rooms, start=1):
            print(f"{i}: {item}")
        while True:
            try:
                choice = int(input("> "))
                if 1 <= choice <= len(name_rooms):
                    selected_rooms = name_rooms[choice - 1]
                    selected_room_rid = rid_rooms[choice - 1]
                    print(f"You selected: {selected_rooms}")
                    print(f"You selected: {selected_room_rid}")
                    url = f"https://{Bridge_IP}/clip/v2/resource/grouped_light/{selected_room_rid}"
                    break
                else:
                    print("Invalid selection")
            except ValueError:
                print("Please enter a valid number")
        return url
    else:
        print (f"{response.status_code}")

def url_zone_selection():
    name_zones=[]
    rid_zones=[]
    url = f"https://{Bridge_IP}/clip/v2/resource/zone"
    response = requests.get(url, headers=headers, timeout=5, verify= False)
    if response.status_code == 200:
        data = response.json()
        for group in data["data"]:
            metadata_data_name_zones = group['metadata']['name']
            name_zones.append(metadata_data_name_zones)
            for service in group["services"]:
                rid_zones.append(service["rid"])
        for i, item in enumerate(name_zones, start=1):
            print(f"{i}: {item}")
        while True:
            try:
                choice = int(input("> "))
                if 1 <= choice <= len(name_zones):
                    selected_zone_name = name_zones[choice - 1]
                    selected_zone_rid = rid_zones[choice - 1]
                    print(f"You selected: {selected_zone_name}")
                    print(f"You selected: {selected_zone_rid}")
                    url = f"https://{Bridge_IP}/clip/v2/resource/grouped_light/{selected_zone_rid}"
                    break
                else:
                    print("Invalid selection")
            except ValueError:
                print("Please enter a valid number:")
        return url
    else:
        print (f"{response.status_code}")

def url_light_selection():
    rid_lights=[]
    name_lights=[]
    url = f"https://{Bridge_IP}/clip/v2/resource/light"
    response = requests.get(url, headers=headers, timeout=5, verify= False)
    if response.status_code == 200:
        data = response.json()
        for group in data["data"]:
            metadata_data = group['metadata']['name']
            name_lights.append(metadata_data)
            for owner in data['data']:
                rid_lights_listing = owner["id"]
                rid_lights.append(rid_lights_listing)
        for i, item in enumerate(name_lights, start=1):
            print(f"{i}: {item}")
        while True:
            try:
                choice = int(input("> "))
                if 1 <= choice <= len(name_lights):
                    selected_light_name = name_lights[choice - 1]
                    selected_light_rid = rid_lights[choice - 1]
                    print(f"You selected: {selected_light_name}")
                    print(f"You selected: {selected_light_rid}")
                    url = f"https://{Bridge_IP}/clip/v2/resource/light/{selected_light_rid}"
                    break
                else:
                    print("Invalid selection")
            except ValueError:
                print("Please enter a valid number")
        return url
    else:
        print (f"{response.status_code}")

if __name__ == "__main__":
    url_room_selection()
    url_zone_selection()
    url_light_selection()