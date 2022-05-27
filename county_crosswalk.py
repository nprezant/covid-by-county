import csv

with open("county_crosswalk.txt", "r") as f:
    r = csv.reader(f, delimiter=",")
    with open("county_crosswalk_processed.txt", "w") as p:
        w = csv.writer(p, delimiter=",", quoting=csv.QUOTE_ALL)
        keep = [0,2,3,4,5,6,7]
        for n,row in enumerate(r):
            if n == 0:
                pass
            elif n == 1:
                w.writerow([row[i] for i in keep] + ["County"])
            else:
                w.writerow([row[i] for i in keep] + [" ".join(row[5].split(" ")[:-1])])
