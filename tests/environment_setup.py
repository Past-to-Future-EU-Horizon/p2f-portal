from uuid import uuid4
from pprint import pprint
from typing import List, Dict
from random import randint, choice
from os import getcwd
from datetime import datetime
import socket
from time import sleep
import docker

# print(getcwd())

def random_port_wcheck():
    port_available = False
    while port_available is False:
        port = randint(8000, 9999)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.bind(("127.0.0.1", port))
            port_available = True
        except socket.error as e:
            errrrrrrrr = e
        finally:
            s.close()
    return port

p2f_portal_port = random_port_wcheck()
test_run_id = uuid4()

client = docker.from_env()

# Stop old portals
old_portals = client.containers.list(all=True)
old_portals = [x for x in old_portals if x.name.startswith("p2f_portal")]
[x.stop() for x in old_portals]
sleep(2)
# Remove old portals
old_portals = client.containers.list(all=True)
old_portals = [x for x in old_portals if x.name.startswith("p2f_portal")]
[x.remove() for x in old_portals]


print(f"The portal will run on http://127.0.0.1:{p2f_portal_port}")

print("Gathering configuration from running Docker P2F-API container")

# Get the latest API Container 
p2f_api_container = client.containers.list()
api_containers = [x for x in client.containers.list() if x.name.startswith("p2f_api_")]
api_containers = {x.attrs["Created"]: x for x in api_containers}
api_containers = {datetime.strptime(f"{x.split('.')[0]}Z", "%Y-%m-%dT%H:%M:%SZ"): y for x, y in api_containers.items()}
api_container = api_containers[max(list(api_containers.keys()))]

# Get the container environment
api_config = api_container.attrs["Config"]["Env"]
# In case there is another = elsewhere in the environment variable (I'm not sure that's possible) we grab the first portion, then slice off the rest
api_config = {x.split("=")[0]: x.replace(f'{x.split("=")[0]}=', '') for x in api_config}

# Get the network of the running API container
api_network_config = api_container.attrs["NetworkSettings"]
api_network = [x for x in api_network_config["Networks"].keys() if x.startswith("p2f_network_test")][0]

# Get the DNS name of the api container within the network, select the first value
api_dns_name = api_network_config["Networks"][api_network]["DNSNames"][0]

# Set the environment
portal_environment = {
    "P2F_PORTAL_EMAIL_ADDRESS": api_config["P2F_PORTAL_EMAIL_ADDRESS"],
    "P2F_PORTAL_TOKEN": api_config["P2F_PORTAL_TOKEN"],
    "P2F_API_HOSTNAME": api_dns_name,
    "P2F_API_PORT": 8084,
    "P2F_API_HTTPS": False,
}



## Import config from p2f-api testing
# api_config = eval(input("Please paste the config from  the p2f-api testing session"))

# pprint(api_config)



def highest_epoch_seconds(history: List[Dict]) -> int:
    rv = 0
    for h in history:
        if h["Created"] > rv:
            rv = h["Created"]
    return rv

p2f_portal_images = client.images.list("p2f-portal*")
p2f_portal_image_ages = {highest_epoch_seconds(x.history()): x.id.split(":")[-1] for x in p2f_portal_images}
p2f_portal_image = p2f_portal_image_ages[max(p2f_portal_image_ages.keys())]

p2f_portal_container_name = f"p2f_portal_{str(hex(test_run_id.fields[-1]))[2:]}"
p2f_portal_container = client.containers.run(image=p2f_portal_image,
                                             remove=True,
                                             environment=portal_environment, 
                                             ports={8082: p2f_portal_port},
                                             detach=True,
                                            #  volumes={str(getcwd()): {"bind": "/p2f/portal", "mode": "ro"}},
                                             name=p2f_portal_container_name, 
                                             network=api_network)