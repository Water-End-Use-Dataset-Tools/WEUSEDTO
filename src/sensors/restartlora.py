
import requests
import time
import subprocess

apikey ="7eb1088964ba810f14e7ce7983ca7064"
url = "http://parsec2.unicampania.it/emoncms/input/list.json?apikey="+apikey
lora_id ="302"

r = requests.get(url)
input_list = r.json()
for input in input_list:
    if input["id"] == lora_id:
        print(input["value"])
        print(input["time"])

        now = time.time()
        print(now)
        if now-int(input["time"]) > 600:
            subprocess.call(["supervisorctl", "-s", "http://localhost:9001", "-u", "cossmic", "-p", "2525",
                             "restart", "lorameter"])
