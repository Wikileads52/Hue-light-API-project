import requests
import json
import os
from time import sleep
from dotenv import load_dotenv

load_dotenv()

#env variable
Bridge_IP = os.getenv("Hue_Bridge_IP")
UserName = os.getenv("Hue_UserName")
Certificate_Path = os.getenv("Certificate_Path")
print(Certificate_Path)

#header
headers= {
    "hue-application-key": UserName,
    "Content-Type": "application/json"
}

rid_lights=[]
name_lights=[]
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
                    #print(f"You selected: {selected_light_name}")
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
    url = url_light_selection()