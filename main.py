import requests
import json
import os
from pprint import pprint

if __name__ == "__main__":

    # Prefer using cached data to avoid unnecessary API calls
    if (os.path.exists("co.json")):
        with open("co.json", "r") as f:
            data = json.load(f)
    else:
        url = "https://data.cdc.gov/resource/3nnm-4jni.json?state=Colorado"
        with open("CovidByCountyKeySecret.txt") as f:
            keyId = f.readline().strip()
            secret = f.readline().strip()
        print(keyId, secret)
        res = requests.get(url, auth=(keyId, secret))

        data = res.json()
        with open("co.json", "w") as f:
            json.dump(data, f, indent=4)

    # Get list of all states

    # Get list of all counties

    # Get relevant, most recent data

    # Get relevant historical data

    # Check when dataset was last updated
    pprint(data)

