import pandas as pd
import requests
import pytest
from src.stock import Stock
from unittest.mock import Mock
from pandas.testing import assert_frame_equal


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
        stock = Stock("TSLA")
        actual = stock.get_weekly_stock_data()
        expected = 'Weekly Time Series'
        message = f"get_weekly_stock_data returned {actual}, did not contain {expected}"

        assert expected in actual, message


class TestCleanStockData(object):
    def test_returns_dataframe_with_correct_cols_and_dtypes(self):
        mock_response_data = {'Weekly Time Series': {
                            '2023-03-24': {
                                '5. volume': '694177636'
                            }
                        }
        }

        stock = Stock("TSLA")
        actual = stock.clean_stock_data(mock_response_data)
        # set expected dataframe data, columns, and datatype
        expected_df = pd.DataFrame({
                                    'date': "2023-03-24",
                                    'volume': pd.Series(694177636.0, dtype="float64"),
                                    'YEAR': pd.Series(2023, dtype="int64")
                               })

        assert_frame_equal(expected_df, actual)

    def test_year_has_typo(self):
        mock_response_data = {'Weekly Time Series': {
                                    '202-03-24': {
                                        '5. volume': '694177636'
                                    }
                               }
        }

        stock = Stock("TSLA")
        actual = stock.clean_stock_data(mock_response_data)

        assert actual is None

    def test_given_response_data_has_missing_volume(self):
        response_data = {
            'Weekly Time Series': {
                '2023-07-09': {
                    '5. volume': '694177636'
                },
                '2023-07-16': {
                    '5. volume': '712075329'
                },
                '2023-07-23': {
                    '4. close': '190.4100'
                }
            }
        }

        stock = Stock("TSLA")
        actual = stock.clean_stock_data(response_data)

        # Should skip rows with missing data
        expected_df = pd.DataFrame({
                                    'date': ["2023-07-09", "2023-07-16"],
                                    'volume': pd.Series([694177636.0, 712075329], index=[0, 1], dtype="float64"),
                                    'YEAR': pd.Series(2023, index=[0, 1], dtype="int64")
                               }, index=[0, 1])
        print(expected_df)
        print(actual)

        assert_frame_equal(expected_df, actual)

    def test_clean_stock_data_missing_key_raises_exception(self):
        mock_response_data = {'Test Time Series': {
                            '2023-03-24': {
                                '5. volume': '694177636'
                            }
                        }
        }
        stock = Stock("TSLA")

        with pytest.raises(KeyError):
            stock.clean_stock_data(mock_response_data)


class TestComputeAvgVolume(object):
    def test_year_count_greater_than_or_equal_to_max_available_data(self):
        # mock df for a newly offered stock on 2020
        mock_df = pd.DataFrame({
                                    'date': ["2023-07-09", "2021-07-16", "2020-07-16"],
                                    'volume': pd.Series([100.0, 200, 300],
                                                        index=[0, 1, 2],
                                                        dtype="float64"),
                                    'YEAR': pd.Series([2023, 2021, 2020], index=[0, 1, 2], dtype="int64")
                               }, index=[0, 1, 2])
        stock = Stock("TSLA")
        actual = stock.compute_avg_volume(mock_df, 7)

        # expected to get all dates from mock_df
        expected = pd.DataFrame({
                                    'STOCK': ["TSLA", "TSLA", "TSLA"],
                                    'YEAR': pd.Series([2020, 2021, 2023], index=[0, 1, 2], dtype="int64"),
                                    'AVERAGE_VOLUME': pd.Series([300, 200, 100.0], index=[0, 1, 2], dtype="float64")
                               }, index=[0, 1, 2])

        assert_frame_equal(expected, actual)

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
