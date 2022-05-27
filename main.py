import requests
import json
import os
import sys
from pprint import pprint


def get_headers():
    with open("ApplicationToken.txt", "r") as f:
        appToken = f.readline().strip()
    return { "X-App-Token": appToken }


def cached_request(url, cache_path):
    if (os.path.exists(cache_path)):
        print("Using cached data in", cache_path, "for", url)
        with open(cache_path, "r") as f:
            return json.load(f)
    else:
        print("Getting new data for", url)
        res = requests.get(url, headers=get_headers())
        if not res.ok:
            raise requests.exceptions.HTTPError("Result not ok", res.status_code, res.content)
        
        data = res.json()
        with open(cache_path, "w") as f:
            json.dump(data, f, indent=4)
        return data


if __name__ == "__main__":

    # Prefer using cached data to avoid unnecessary API calls
    # Get covid data for colorado
    co = cached_request("https://data.cdc.gov/resource/3nnm-4jni.json?state=Colorado", "co.json")
    
    # pprint(co_data)

    # Get list of all states
    states_data = cached_request("https://data.cdc.gov/resource/3nnm-4jni.json?$select=distinct(state) as state", "states.json")
    states = [x["state"] for x in states_data]
    states.sort()
    print("States:", states[:4], "...")

    # Get list of all counties
    counties = list(set([x["county"] for x in co]))
    counties.sort()
    print("Counties:", counties[:4], "...")

    # Get relevant, most recent data
    county_name = "Larimer County"
    larimer_historical = [x for x in co if x["county"] == county_name]
    larimer_historical.sort(key=lambda x: x["date_updated"], reverse=True)
    pprint(larimer_historical[0])

    # Get relevant historical data
    historical_levels = [(x["date_updated"], x["covid_19_community_level"]) for x in larimer_historical]
    print("Previous levels")
    pprint(historical_levels)

    # Check when dataset was last updated
    # Checking for dataset metadata is done through the discovery API.
    catelog = cached_request("http://api.us.socrata.com/api/catalog/v1?ids=3nnm-4jni", "catelog.json")
    updated_at = catelog["results"][0]["resource"]["updatedAt"]
    print("Dataset last updated at ", updated_at)

    # Get transmission level data
    transmissions = cached_request("https://data.cdc.gov/resource/8396-v7yb.json?state_name=Colorado", "transmissions.json")
    larimer_transmissions = [x for x in transmissions if x["county_name"] == "Larimer County"]
    pprint(larimer_transmissions[-1])
    print("Number of larimer transmissions recorded:", len(larimer_transmissions))

    # Get states and counties
    #st_ct = cached_request("https://data.cdc.gov/resource/3nnm-4jni.json?$query=SELECT DISTINCT state,county WHERE state LIKE %co% OR county LIKE %co% LIMIT 10", "st_ct.json")
    st_ct = cached_request("https://data.cdc.gov/resource/3nnm-4jni.json?$query=SELECT DISTINCT state,county LIMIT 10", "st_ct.json")
