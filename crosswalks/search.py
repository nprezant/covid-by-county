"""
Search through the counties for a match
"""

import csv
from dataclasses import dataclass
from typing import List


def rankmatch(text, base, debug=False) -> int:
    """Ranks how well text matches the base
      b a s e
    t 0 0 0 0
    e 0 0 0 1
    x 0 0 0 0
    t 0 0 0 0

    Apply weights.
    Sequences of characters are weighted more heavily than individuals.
    First letter of word matches are weighted more heavily
        2  8  7  8  7
    -----------------
    2 | 1  0  0  0  0
    8 | 0  1  0  0  0
    7 | 0  0  1  0  1
    8 | 0  0  0  1  0
    7 | 0  0  0  0  1
    
        2  8  7  8  7
    -----------------
    2 | 1  2  3  4  5
    8 | 0  1  2  3  4
    7 | 0  0  1  2  3
    8 | 0  0  0  1  2
    7 | 0  0  0  0  1
    
        2  8  7  8  7
    -----------------
    2 | 1  2  3  4  5
    8 | 0  1  2  3  4
    7 | 0  0  1  2  3
    8 | 0  1  2  1  2
    7 | 0  0  1  0  1
    """
    text = text.lower()
    base = base.lower()
    rankings = [0] * (len(text) * len(base))

    def get_index(i, j):
        return (j * len(base)) + i

    # Determine character matches
    for j in range(0, len(text)): # Each letter in text
        for i in range(0, len(base)): # Each letter in base
            if text[j] == base[i]:
                index = get_index(i, j)
                rankings[index] = 1

    if debug:
        print_rank_table(text, base, rankings)

    for i in range(1, len(base)):
        for j in range(len(text)-2, -1, -1):
            under = rankings[get_index(i, j+1)]
            left = rankings[get_index(i-1, j)]
            # isAtStart = j == 0
            # isNewWord = isAtStart or rankings[index - 1] == ' '
            if under != 0 and left != 0:
                if under == left:
                    rankings[get_index(i, j)] = left + 1

    if debug:
        print_rank_table(text, base, rankings)

    return sum(rankings) 

def print_rank_table(text, base, rankings):
    print("  " + "".join(f"  {x}" for x in base))
    print("--" + "".join(f"---" for _ in base))
    for i in range(0, len(text)):
        print(text[i] + " | ", end="")
        for j in range(0, len(base)):
            index = (i * len(base)) + j
            print(f"{'' if j == 0 else '  '}{rankings[index]}", end="")
        print()

@dataclass
class MatchItem:
    quality: int
    text: str

def rankmatchlist(text, choices: List[str]) -> MatchItem:
    """Find the best match from a list of choices"""
    matches = [MatchItem(rankmatch(text, choice), choice) for choice in choices]
    return max(matches, key=lambda x: x.quality)

@dataclass
class CountyMatch:
    county: str
    match: MatchItem

def search(text, limit) -> List[CountyMatch]:
    with open("processed/county-all.csv", "r") as f:
        r = csv.reader(f, delimiter=",", quoting=csv.QUOTE_ALL)
        county_matches = [CountyMatch(line[0], rankmatchlist(text, line)) for line in r]
    county_matches.sort(key=lambda x: x.match.quality, reverse=True)
    limit = min(limit, len(county_matches))
    return county_matches[:limit]

def test_rank(text, base, debug=False):
    print(f"Rank of '{text}' in '{base}' is {rankmatch(text, base, debug)}")

def test_ranklist(text, baselist):
    print(f"Rank of '{text}' in '{baselist}' is {rankmatchlist(text, baselist)}")

def test_search(text, limit):
    print(f"Searching for '{text}'")
    for match in search(text, limit):
        print(f"{match.match.quality}, {match.county}, found with '{match.match.text}'")

if __name__ == "__main__":
    # test_rank("A", "Asheville")
    # test_rank("As", "Asheville")
    # test_rank("Ash", "Asheville")
    # test_rank("Ashe", "Asheville")

    # test_ranklist("Asheville", ["Asheville", "North Carolina"])
    # questionable = ["Davidson County, Tennessee","37011","37013","37015","37024","37027","37064","37070","37072","37073","37076","37080","37086","37115","37116","37122","37135","37138","37143","37189","37201","37202","37203","37204","37205","37206","37207","37208","37209","37210","37211","37212","37213","37214","37215","37216","37217","37218","37219","37220","37221","37222","37224","37227","37228","37229","37232","37234","37235","37236","37238","37240","37242","37243","37246","37250","Belle Meade","Berry Hill","Forest Hills","Goodlettsville","Lakewood","Nashville-Davidson","Oak Hill","Ridgetop"]
    # for q in questionable:
    #     test_rank("Asheville", q)

    # test_rank("Asheville", "Milledgeville", True)
    # test_rank("Asheville", "Asheville", True)
    test_rank("28787", "28787-15", True)
    test_rank("28787", "28777", True)

    # test_search("Asheville", 3)
    # test_search("28787", 3)
    # test_search("Teton", 3)
    # test_search("Teton, Wyoming", 3)
    test_search("Teton Co, Wyoming", 3)
    test_search("Jackson", 3)
    test_search("Jackson, WY", 3)
    test_search("Jackson, Wyoming", 3)
