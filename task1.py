import requests
import os
import pandas as pd
import datetime

# set parameter values
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
ALPHAVANTAGE_KEY = os.environ.get("ALPHA_KEY")
STOCK = "TSLA"
YEAR_THRESHOLD = 4

# TODO 1: Connect to alphavantage API and retrieve stock data
alpha_param = {
    "function": "TIME_SERIES_WEEKLY",
    "symbol": STOCK,
    "apikey": ALPHAVANTAGE_KEY,
    "datatype": "json"
}

response = requests.get(STOCK_ENDPOINT, params=alpha_param)
data = response.json()

# TODO 2: From the response, create a dataframe that contains year and volume
weekly_df = pd.DataFrame.from_dict(data['Weekly Time Series'],
                                   orient='index',
                                   columns=['5. volume']
                                   )

clean_weekly_df = weekly_df.reset_index(names='date') \
    .rename(columns={'5. volume': 'volume'})

# add year column
clean_weekly_df['YEAR'] = clean_weekly_df['date'].str[0:4] \
    .astype(int)
# set datatype
clean_weekly_df['volume'] = clean_weekly_df['volume'].astype(float)

# TODO 3: Get the average volume per year for the past 5 years for the selected stock

# compute past 5 years
year_filter = int(datetime.date.today().year) - YEAR_THRESHOLD

# filter, aggregate and fix schema
vol_by_year_df = clean_weekly_df.query(f'YEAR >= {year_filter}') \
    .groupby('YEAR').mean(numeric_only=True) \
    .rename(columns={"volume": "AVERAGE_VOLUME"}) \
    .assign(STOCK=STOCK) \
    .reset_index()

# TODO 4:output the df into a csv file with columns STOCK, YEAR, AVERAGE_VOLUME
vol_by_year_df[['STOCK', 'YEAR', 'AVERAGE_VOLUME']].to_csv(f"{STOCK}_average_vol_per_year.csv", index=False)
