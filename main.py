import requests
import os
import pandas as pd

# TODO 1: Connect to alphavantage API and retrieve stock data
STOCK_ENDPOINT = "https://www.alphavantage.co/quer"
ALPHAVANTAGE_KEY = os.environ.get("ALPHA_KEY")
STOCK = "TSLA"

alpha_param = {
    "function": "TIME_SERIES_MONTHLY",
    "symbol": STOCK,
    "apikey": ALPHAVANTAGE_KEY
}

response = requests.get(STOCK_ENDPOINT, params=alpha_param)
data = response.json()
print(data)
# TODO 2: From the response, get the volume of Tesla stock
# TODO 3: Get the average volume per year, output columns should be STOCK, YEAR, AVERAGE_VOLUME
