import requests
import json
import os
import urllib3
import ssl
import socket
from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager
from time import sleep

Bridge_IP = os.getenv("Hue_Bridge_IP")
UserName = os.getenv("Hue_UserName")

headers= {
    "Content-Type": "application/json"
}

def get_bridge_id_ip_port():
    url = "https://discovery.meethue.com"
    response = requests.get(url, headers = headers, timeout=5)
    if response.status_code == 200:
        data = response.json()
        with open ("this_file.txt", "w") as file:
            json.dump(data , file)
        return data
    else:
        print(f"{response.status_code}")

data = get_bridge_id_ip_port()
bridge = data[0]
bridge_id = data[0]["id"]
bridge_ip = data[0]["internalipaddress"]
bridge_port = data[0]["port"]

class Hue_Https_Adapter(HTTPAdapter):
    def __init__(self, bridge_ip, bridge_id, CA_bundle_path, **kwargs):
        self.bridge_ip = bridge_ip
        self.bridge_id = bridge_id
        self.CA_bundle_path = "hue_ca.pem"
        super().__init__(**kwargs)

    def init_poolmanager(self, connections, maxsize, block=False):
        context = ssl.create_default_context(cafile=self.ca_bundle)

        self.poolmanager = PoolManager(
            num_pools=connections,
            maxsize=maxsize,
            block=block,
            ssl_context=context,
            assert_hostname=self.bridge_id
        )

    def get_connection(self, url, proxies=None):
        # Force connection to bridge IP instead of DNS
        return self.poolmanager.connection_from_host(
            host=self.bridge_ip,
            port=443,
            scheme="https"
        )



def verify_bridge_connection(data):
    headers= {
    "hue-application-key": UserName,
    "Content-Type": "application/json" 
    }   
    bridge = data[0]
    bridge_id = data[0]["id"]
    bridge_ip = data[0]["internalipaddress"]
    bridge_port = data[0]["port"]
    #print (bridge_id, bridge_ip, bridge_port)
    CA_bundle_path = "hue_ca.pem"
    testing_url = f"https://{bridge_id}:{bridge_port}/clip/v2/resource/light"
    response = requests.get(testing_url, headers = headers, timeout=5, verify= CA_bundle_path)
    if response.status_code == 200:
        data = response.json
        print(data)
    else:
        print(f"{response.status_code}")
verify_bridge_connection(data)