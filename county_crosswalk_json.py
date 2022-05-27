
import json
import csv

with open("county_crosswalk.txt", "r") as f:
    r = csv.reader(f, delimiter=",")
    keep = [0,2,3,4,5,6,7]
    headers = []
    data = []
    for n,row in enumerate(r):
        if n == 0:
    	    pass
        elif n == 1:
    	    headers = [row[i] for i in keep] + ["County"] 
        else:
            data.append({headers[i]: row[i] for i in keep})
            data[-1]["County"] = " ".join(row[5].split(" ")[:-1])
with open("county_crosswalk_processed.json", "w") as p:
    json.dump(data, p)
