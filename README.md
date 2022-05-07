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
