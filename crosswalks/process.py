"""
Process the raw crosswalk data
"""

from collections import defaultdict
import csv
from typing import Dict, Tuple


statenames = {
    "AK": "Alaska",
    "AL": "Alabama",
    "AR": "Arkansas",
    "AS": "American Samoa",
    "AZ": "Arizona",
    "CA": "California",
    "CO": "Colorado",
    "CT": "Connecticut",
    "DC": "District of Columbia",
    "DE": "Delaware",
    "FL": "Florida",
    "GA": "Georgia",
    "GU": "Guam",
    "HI": "Hawaii",
    "IA": "Iowa",
    "ID": "Idaho",
    "IL": "Illinois",
    "IN": "Indiana",
    "KS": "Kansas",
    "KY": "Kentucky",
    "LA": "Louisiana",
    "MA": "Massachusetts",
    "MD": "Maryland",
    "ME": "Maine",
    "MI": "Michigan",
    "MN": "Minnesota",
    "MO": "Missouri",
    "MS": "Mississippi",
    "MT": "Montana",
    "NC": "North Carolina",
    "ND": "North Dakota",
    "NE": "Nebraska",
    "NH": "New Hampshire",
    "NJ": "New Jersey",
    "NM": "New Mexico",
    "NV": "Nevada",
    "NY": "New York",
    "OH": "Ohio",
    "OK": "Oklahoma",
    "OR": "Oregon",
    "PA": "Pennsylvania",
    "PR": "Puerto Rico",
    "RI": "Rhode Island",
    "SC": "South Carolina",
    "SD": "South Dakota",
    "TN": "Tennessee",
    "TX": "Texas",
    "UT": "Utah",
    "VA": "Virginia",
    "VI": "Virgin Islands",
    "VT": "Vermont",
    "WA": "Washington",
    "WI": "Wisconsin",
    "WV": "West Virginia",
    "WY": "Wyoming"
}

def process_zips():
    # Map fips codes to a list of associated zip codes
    zip_data = defaultdict(set)
    with open("raw/zip-county.csv", "r") as f:
        r = csv.reader(f, delimiter=",")
        next(r)
        for row in r:
            countyfp = row[3]
            zip = row[0]
            zip_data[countyfp].add(zip)

    with open("processed/county-zips.csv", "w") as f:
        w = csv.writer(f, delimiter=",", quoting=csv.QUOTE_ALL)
        w.writerow(["STCOUNTYFP", "ZIPS,..."])
        for countyfp,zips in zip_data.items():
            w.writerow([countyfp] + sorted(list(zips)))

def get_countyfp_names() -> Dict[int,Tuple[str,str]]:
    """ Match fips codes to a county name """
    m = {}
    # Fill in a few missing values
    m[46102] = "Oglala Lakota County", "SD"
    m[46113] = "Shannon County", "SD"
    with open("raw/zip-county.csv", "r") as f:
        r = csv.reader(f, delimiter=",")
        next(r)
        for row in r:
            countyfp = row[3]
            county = row[1]
            state = row[2]
            m[countyfp] = county, state
    return m

def write_countyfp_names():
    """ Write out table: COUNTYFP,COUNTYNAME,STATE """
    with open("processed/countyfp-county.csv", "w") as f:
        f.write("COUNTYFP,COUNTYNAME,STATE\n")
        for fp,(county,state) in get_countyfp_names().items():
            f.write(f'"{fp}","{county}","{state}"\n')

def write_state_list():
    states = set()
    for fp,(county,state) in get_countyfp_names().items():
        states.add(state)

    with open("processed/short-states.txt", "w") as f:
        for s in sorted(states):
            f.write(f'"{s}": "",\n')

def inverted(d: dict) -> dict:
    """ Invert key-value pairs """
    return {v:k for k,v in d.items()}

def process_places():
    """ Map fips codes to a list of associated places """
    # County name (not fips) provided in table.
    # Map (county,state) to a fips code
    countyfpmap = inverted(get_countyfp_names())

    place_data = defaultdict(set)
    with open("raw/ansi_places.csv", "r", encoding="latin-1") as f:
        r = csv.reader(f, delimiter="|")
        next(r)
        for row in r:
            if len(row) == 0:
                continue
            place = row[3]
            state = row[0]
            counties = [x.strip() for x in row[6].split(",")]
            # print(counties)
            for county in counties:
                cleaned = county.replace("ñ", "n")
                countyfp = countyfpmap.get((cleaned, state), None)
                if countyfp is None:
                    print("No fips code found for ", cleaned, ",", state)
                else:
                    place_data[countyfp].add(place)

    with open("processed/county-places.csv", "w") as f:
        w = csv.writer(f, delimiter=",", quoting=csv.QUOTE_ALL)
        w.writerow(["STCOUNTYFP", "PLACES,..."])
        for countyfp,places in place_data.items():
            w.writerow([countyfp] + sorted(list(places)))

def process_combined():
    """
    Create combined file of counties mapped to states, zips, and places
    """
    zips = {}
    states = {}
    names = {}
    places = {}

    with open("processed/county-zips.csv", "r") as f:
        r = csv.reader(f, delimiter=",", quoting=csv.QUOTE_ALL)
        next(r)
        for row in r:
            countyfp = row[0]
            ziplist = row[1:]
            zips[countyfp] = ziplist
    
    with open("processed/county-places.csv", "r") as f:
        r = csv.reader(f, delimiter=",", quoting=csv.QUOTE_ALL)
        next(r)
        for row in r:
            countyfp = row[0]
            placelist = [place.rsplit(" ", maxsplit=1)[0] for place in row[1:]] # Remove census place type
            placelist = [place.removesuffix(" metropolitan government") for place in placelist]
            places[countyfp] = placelist
    
    with open("processed/countyfp-county.csv", "r") as f:
        r = csv.reader(f, delimiter=",", quoting=csv.QUOTE_ALL)
        next(r)
        for row in r:
            countyfp = row[0]
            county = row[1]
            state = row[2]
            states[countyfp] = state
            names[countyfp] = county

    with open("processed/county-all.csv", "w") as f:
        w = csv.writer(f, delimiter=",", quoting=csv.QUOTE_ALL)
        for fip in zips.keys():
            name = names.get(fip, "")
            state = statenames.get(states.get(fip, ""))
            ziplist = zips.get(fip, [])
            placelist = places.get(fip, [])
            w.writerow([f"{name}, {state}"] + ziplist + placelist)

if __name__ == "__main__":
    
    # Find all zip codes associated with each county.
    process_zips()
    write_countyfp_names()
    write_state_list()
    process_places()
    process_combined()
