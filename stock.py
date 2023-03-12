import requests
import pandas as pd
import datetime
import os

# set the average volume per year for the past (YEAR_THRESHOLD + 1) years including current year
YEAR_THRESHOLD = 4


class Stock:
    STOCK_ENDPOINT = "https://www.alphavantage.co/query"
    ALPHAVANTAGE_KEY = os.environ.get("ALPHA_KEY")

    def __init__(self, stock_name):
        self.stock_name = stock_name

    # TODO 1: Connect to alphavantage API and retrieve stock data
    def get_weekly_stock_data(self):
        """"Retrieve stock data from Alphavantage API."""
        try:
            alpha_param = {
                "function": "TIME_SERIES_WEEKLY",
                "symbol": self.stock_name,
                "apikey": Stock.ALPHAVANTAGE_KEY,
                "datatype": "json"
            }

            response = requests.get(Stock.STOCK_ENDPOINT, params=alpha_param)
            response_data = response.json()
            return response_data
        except requests.exceptions.RequestException as e:
            print(f"error retrieving stock data: {e}")
            return None

    # TODO 2: From the response, create a dataframe that contains year and volume
    @staticmethod
    def clean_stock_data(response_data):
        """Clean and preprocess stock data."""
        weekly_df = pd.DataFrame.from_dict(response_data['Weekly Time Series'],
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
        return clean_weekly_df

    # TODO 3: Get the average volume per year for the past 5 years for the selected stock
    def compute_avg_volume(self, df):
        """Compute the average volume per year for the past (YEAR_THRESHOLD + 1) years including current year"""
        # compute past 5 years
        year_filter = int(datetime.date.today().year) - YEAR_THRESHOLD

        # filter, aggregate and fix schema
        vol_by_year_df = df.query(f'YEAR >= {year_filter}') \
            .groupby('YEAR') \
            .mean(numeric_only=True) \
            .rename(columns={"volume": "AVERAGE_VOLUME"}) \
            .assign(STOCK=self.stock_name) \
            .reset_index()
        return vol_by_year_df[['STOCK', 'YEAR', 'AVERAGE_VOLUME']]

    # TODO 4:output the df into a csv file with columns STOCK, YEAR, AVERAGE_VOLUME
    def save_data_to_csv(self, df):
        """Save the DataFrame to a CSV file."""
        file_name = f"{self.stock_name}_average_vol_per_year.csv"
        with open(file_name, 'w') as f:
            df.to_csv(f"{self.stock_name}_average_vol_per_year.csv", index=False)
