import pytest
from src.stock import Stock


class TestGetWeeklyStockData(object):
    def test_given_code_is_not_a_stock(self):
        pass

    def test_on_api_failed_connection(self):
        pass

    def test_on_a_us_stock(self):
        pass


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
