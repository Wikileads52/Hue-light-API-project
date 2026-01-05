import requests
import json
import os
from time import sleep
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

name_zones=[]
rid_zones=[]
def url_zone_selection():
    name_zones=[]
    rid_zones=[]
    url = f"https://{Bridge_IP}/clip/v2/resource/zone"
    response = requests.get(url, headers=headers, timeout=5, verify= False)
    if response.status_code == 200:
        data = response.json()
        #print(data["data"])
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
                    #print(f"You selected: {selected_zone_rid}")
                    url = f"https://{Bridge_IP}/clip/v2/resource/grouped_light/{selected_zone_rid}"
                    #print (url)
                    break
                else:
                    print("Invalid selection")
            except ValueError:
                print("Please enter a valid number:")
        return url
    else:
        print (f"{response.status_code}")

if __name__ == "__main__":
    url = url_zone_selection()
