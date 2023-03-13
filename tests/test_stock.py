import requests
import pytest
from src.stock import Stock
from unittest.mock import Mock


class TestGetWeeklyStockData(object):
    def test_given_code_is_not_a_stock(self):
        stock = Stock("AWWW")
        actual = stock.get_weekly_stock_data()
        expected = None
        message = f"get_weekly_stock_data returned {actual} instead of {expected}"
        assert actual is expected, message

    def test_on_api_failed_connection(self, mocker):
        # Replace the requests.get function with a mock function that raises a requests.exceptions.RequestException
        mocker.patch("requests.get", side_effect=requests.exceptions.RequestException)

        # Create a new Stock object and call the get_weekly_stock_data method
        stock = Stock("TSLA")
        result = stock.get_weekly_stock_data()

        # Check that the result is None
        assert result is None

    def test_on_a_us_stock(self):
        stock = Stock("CEB")
        actual = stock.get_weekly_stock_data()
        expected = 'Weekly Time Series'
        message = f"get_weekly_stock_data returned {actual}, did not contain {expected}"
        assert expected in actual, message


class TestCleanStockData(object):
    def test_given_data_is_not_from_api(self):
        pass

    def test_given_data_is_from_api(self):
        pass

    def test_wrong_function(self):
        pass


class TestComputeAvgVolume(object):
    def test_max_year_count(self):
        pass

    def test_year_count_greater_than_max(self):
        pass

    def test_min_year_count(self):
        pass

    def test_year_count_less_than_min(self):
        pass

    def test_default_year_count(self):
        pass

    def test_year_count_not_a_number(self):
        pass

    def test_given_a_valid_year_count(self):
        pass


class TestSaveDataToCsv(object):
    def test_given_data_is_not_a_df(self):
        pass

    def test_file_is_already_existing(self):
        pass

    def test_file_data_is_a_df(self):
        pass

    def test_file_is_not_existing(self):
        pass
