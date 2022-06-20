"""
Search through the counties for a match
"""

import csv
from typing import List, Tuple


def rankmatch(text, base, debug=False) -> int:
    """Ranks how well text matches the base
       b a s e
     t 0 0 0 0
     e 0 0 0 1
     x 0 0 0 0
     t 0 0 0 0
    """
    x = len(text)
    y = len(base)
    text = text.lower()
    base = base.lower()
    rankings = [0] * (x * y)
    for i in range(0,x): # Each letter in text
        for j in range(0,y): # Each letter in base
            if text[i] == base[j]:
                index = (i * y) + j
                rankings[index] = 1
                if j != 0:
                    for idx in range(index - y, 0, -y):
                        last_val = rankings[idx - 1]
                        if last_val != 0:
                            rankings[idx] = last_val + 1
    if debug:
        print(" " + "".join(f"  {x}" for x in base))
        for i in range(0, x):
            print(text[i], end="")
            for j in range(0, y):
                index = (i * y) + j
                print(f"  {rankings[index]}", end="")
            print()

    return sum(rankings) 

def rankmatchlist(text, baselist) -> int:
    return max(rankmatch(text, base) for base in baselist)

def search(text, limit) -> List[Tuple[str,int]]:
    qualities = []
    with open("processed/county-all.csv", "r") as f:
        r = csv.reader(f, delimiter=",", quoting=csv.QUOTE_ALL)
        qualities = [(line[0], rankmatchlist(text, line)) for line in r]
    qualities.sort(key=lambda x: x[1], reverse=True)
    limit = min(limit, len(qualities))
    return qualities[:limit]

def test_rank(text, base, debug=False):
    print(f"Rank of '{text}' in '{base}' is {rankmatch(text, base, debug)}")

def test_ranklist(text, baselist):
    print(f"Rank of '{text}' in '{baselist}' is {rankmatchlist(text, baselist)}")

if __name__ == "__main__":
    test_rank("A", "Asheville")
    test_rank("As", "Asheville")
    test_rank("Ash", "Asheville")
    test_rank("Ashe", "Asheville")

    test_ranklist("Asheville", ["Asheville", "North Carolina"])
    questionable = ["Davidson County, Tennessee","37011","37013","37015","37024","37027","37064","37070","37072","37073","37076","37080","37086","37115","37116","37122","37135","37138","37143","37189","37201","37202","37203","37204","37205","37206","37207","37208","37209","37210","37211","37212","37213","37214","37215","37216","37217","37218","37219","37220","37221","37222","37224","37227","37228","37229","37232","37234","37235","37236","37238","37240","37242","37243","37246","37250","Belle Meade","Berry Hill","Forest Hills","Goodlettsville","Lakewood","Nashville-Davidson","Oak Hill","Ridgetop"]
    for q in questionable:
        test_rank("Asheville", q)

    test_rank("Asheville", "Milledgeville", True)
    test_rank("Asheville", "Asheville", True)

    matches = search("Asheville", 3)
    for candidate,quality in matches:
        if quality > 0:
            print(quality, candidate)
