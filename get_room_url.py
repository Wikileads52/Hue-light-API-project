import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

#env variable
Bridge_IP = os.getenv("Hue_Bridge_IP")
UserName = os.getenv("Hue_UserName")


#header
headers= {
    "hue-application-key": UserName,
    "Content-Type": "application/json"
}

name_rooms=[]
rid_rooms=[]

def url_room_selection():
    name_rooms=[]
    rid_rooms=[]
    url = f"https://{Bridge_IP}/clip/v2/resource/room"
    response = requests.get(url, headers=headers, timeout=5, verify= False)
    if response.status_code == 200:
        data = response.json()
        #print(data["data"])
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
                    #print(url)
                    break
                else:
                    print("Invalid selection")
            except ValueError:
                print("Please enter a valid number")
        return url
    else:
        print (f"{response.status_code}")


if __name__ == "__main__":
    url = url_room_selection()
