# Stock Volume Data Retrieval

This project provides a Python script that retrieves stock volume data from Alpha Vantage API and saves it to a CSV file using pandas. It also includes pytest unit tests to ensure the script functions as expected. To run the project, you'll need to have Python 3 installed on your system, as well as the dependencies in the requirements.txt file.

## Installation
You can install the dependencies using pip and the requirements.txt file included in this repository. Simply navigate to the project directory and run the following command:

`pip install -r requirements.txt`

##Usage
To use the project, simply run the main script with your chosen stock and num of years as parameters:
`python main.py TWTR 7`

num of years is optional, default number of years is 5
`python main.py TWTR`

Alpha Vantage provides a number of APIs for retrieving stock market and cryptocurrency
information: https://www.alphavantage.co/documentation/.


