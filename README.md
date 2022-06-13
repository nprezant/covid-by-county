# Covid by county

The dataset we want
https://dev.socrata.com/foundry/data.cdc.gov/3nnm-4jni

Another way to view the data we want. This is updated weekly with the overall community level
https://data.cdc.gov/Public-Health-Surveillance/United-States-COVID-19-Community-Levels-by-County/3nnm-4jni

Dataset updated daily with community transmission level
https://data.cdc.gov/Public-Health-Surveillance/United-States-COVID-19-County-Level-of-Community-T/8396-v7yb

Dev portal for socrata
https://dev.socrata.com/

Dev portal for cdc data
https://data.cdc.gov/login

App token required --> login required
May want to use app token for actual app so that requests are chill and not throttled.
For app token, use X-App-Token in header
https://dev.socrata.com/docs/app-tokens.html

Normal api key fine for scripts.

Getting metadata from socrata is for sure a thing
https://odn.docs.apiary.io/#introduction/app-tokens
Can use for *suggestions* when typing a county/state

Update times...
https://api.us.socrata.com/api/catalog/v1
https://opendata.stackexchange.com/questions/10761/get-metadata-from-all-datasets-on-socrata

# Searching for Counties

Need to be able to search state, county, city, or zip.

Can get crosswalk for state --> county:
https://www.nber.org/research/data/ssa-federal-information-processing-series-fips-state-and-county-crosswalk
Name: crosswalks/raw/county-state-crosswalk.csv

Can get crosswalk for zip code --> county --> state:
https://www.kaggle.com/datasets/danofer/zipcodes-county-fips-crosswalk
Name: crosswalks/raw/zip-county.csv

Can get crosswalk for place (city) --> county:
https://data.world/nrippner/ansi-geographic-codes/workspace/file?filename=ansi_places.csv
Name: crosswalks/raw/ansi-places.csv

Want to be able to look up anything and get a county in return.

- Middlesex County, Colorado 80518 80519 Lansing
- <county>, <long-state> <zips...> <places...>

May be able to create an index for faster searches.
For each alphabetic character and each number, score each county

Questions:

- How many unique counties are there?
- Zips associated with each county
- Places associated with each county

Characters to clean:
�
