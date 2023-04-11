import pandas as pd
import requests
import pytest
from src.stock import Stock
from pandas.testing import assert_frame_equal
import os


class TestGetWeeklyStockData(object):
    def test_given_code_is_not_a_stock(self):
        """assert that function will return None If given code is not a stock"""
        stock = Stock("AWWW")
        actual = stock.get_weekly_stock_data()
        expected = None
        message = f"get_weekly_stock_data returned {actual} instead of {expected}"
        assert actual is expected, message

    def test_on_api_failed_connection(self, mocker):
        """assert that function will return None if API request failed """
        # Replace the requests.get function with a mock function that raises a requests.exceptions.RequestException
        mocker.patch("requests.get", side_effect=requests.exceptions.RequestException)

        # Create a new Stock object and call the get_weekly_stock_data method
        stock = Stock("TSLA")
        result = stock.get_weekly_stock_data()

        # Check that the result is None
        assert result is None

    def test_on_a_us_stock(self):
        """test happy path, assert that function wil return Weekly Time Series given a stock code"""
        stock = Stock("TSLA")
        actual = stock.get_weekly_stock_data()
        expected = 'Weekly Time Series'
        message = f"get_weekly_stock_data returned {actual}, did not contain {expected}"

        assert expected in actual, message


class TestCleanStockData(object):
    def test_returns_dataframe_with_correct_cols_and_dtypes(self):
        """happy path, assert function will return a dataframe with date:yyyy-mm-dd, volume:int, YEAR:int columns"""
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
        """assert that the function will return None if year parsed from date column is not in year format"""
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
        """assert that function will skip rows with missing volume data"""
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

        assert_frame_equal(expected_df, actual)

    def test_clean_stock_data_missing_key_raises_exception(self):
        """assert that function will return an error if given API response does not contain Weekly Time Series key"""
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
    df_test_compute_avg_vol = pd.DataFrame({
        'date': ["2023-07-09", "2021-07-16", "2020-07-16", "2022-04-09", "2019-12-01", "2018-02-16"],
        'volume': pd.Series([100.0, 200, 300, 350.43, 120, 220.6],
                            index=[0, 1, 2, 3, 4, 5],
                            dtype="float64"),
        'YEAR': pd.Series([2023, 2021, 2020, 2022, 2019, 2018], index=[0, 1, 2, 3, 4, 5], dtype="int64")
    }, index=[0, 1, 2, 3, 4, 5])

    def test_year_count_greater_than_or_equal_to_max_available_data(self):
        """assert that function will return correct average computation"""

        df_max_test = TestComputeAvgVolume.df_test_compute_avg_vol.copy()
        df_max_test.loc[len(df_max_test)] = ["2023-01-05", 150.00, 2023]
        stock = Stock("TSLA")
        actual = stock.compute_avg_volume(df_max_test, 7)

        # expected to get correct computed volume for 2023 from df_max_test
        expected = pd.DataFrame({
                                    'STOCK': ["TSLA", "TSLA", "TSLA", "TSLA", "TSLA", "TSLA"],
                                    'YEAR': pd.Series([2018, 2019, 2020, 2021, 2022, 2023], index=[0, 1, 2, 3, 4, 5], dtype="int64"),
                                    'AVERAGE_VOLUME': pd.Series([220.6, 120, 300, 200, 350.43, 125.0], index=[0, 1, 2, 3, 4, 5], dtype="float64")
                               }, index=[0, 1, 2, 3, 4, 5])

        assert_frame_equal(expected, actual)

    def test_min_year_count(self):
        """assert that function will return correct values at smallest year_filter value possible"""
        test_df = TestComputeAvgVolume.df_test_compute_avg_vol
        stock = Stock("TSLA")
        actual = stock.compute_avg_volume(test_df, 1)

        # expected to get 1 date from test_df
        expected = pd.DataFrame({
                                    'STOCK': ["TSLA"],
                                    'YEAR': pd.Series([2023], index=[0], dtype="int64"),
                                    'AVERAGE_VOLUME': pd.Series([100.0], index=[0], dtype="float64")
                               }, index=[0])

        assert_frame_equal(expected, actual)

    def test_year_count_less_than_min(self):
        """assert that function will return None at year_filter less than minimum"""
        test_df = TestComputeAvgVolume.df_test_compute_avg_vol
        stock = Stock("TSLA")
        actual = stock.compute_avg_volume(test_df, 0)

        assert actual is None

    def test_default_year_count(self):
        """assert that function will return 5 years of data if no year_filter parameter is given"""
        test_df = TestComputeAvgVolume.df_test_compute_avg_vol
        stock = Stock("TSLA")
        actual = stock.compute_avg_volume(test_df)

        expected = pd.DataFrame({
                                    'STOCK': ["TSLA", "TSLA", "TSLA", "TSLA", "TSLA"],
                                    'YEAR': pd.Series([2019, 2020, 2021, 2022, 2023], index=[0, 1, 2, 3, 4], dtype="int64"),
                                    'AVERAGE_VOLUME': pd.Series([120, 300, 200, 350.43, 100.0], index=[0, 1, 2, 3, 4], dtype="float64")
                               }, index=[0, 1, 2, 3, 4])

        assert_frame_equal(expected, actual)

    def test_given_a_valid_year_count(self):
        """test happy path"""

        test_df = TestComputeAvgVolume.df_test_compute_avg_vol
        stock = Stock("TSLA")
        actual = stock.compute_avg_volume(test_df, 7)

        # expected to get all dates from test_df
        expected = pd.DataFrame({
                                    'STOCK': ["TSLA", "TSLA", "TSLA", "TSLA", "TSLA", "TSLA"],
                                    'YEAR': pd.Series([2018, 2019, 2020, 2021, 2022, 2023], index=[0, 1, 2, 3, 4, 5], dtype="int64"),
                                    'AVERAGE_VOLUME': pd.Series([220.6, 120, 300, 200, 350.43, 100.0], index=[0, 1, 2, 3, 4, 5], dtype="float64")
                               }, index=[0, 1, 2, 3, 4, 5])

        assert_frame_equal(expected, actual)

    def test_year_count_not_a_number(self):
        """assert that function will return None if given year count is not a number"""
        test_df = TestComputeAvgVolume.df_test_compute_avg_vol
        stock = Stock("TSLA")
        actual = stock.compute_avg_volume(test_df, 'foo')

        assert actual is None


class TestSaveDataToCsv(object):
    test_save_data_df = pd.DataFrame({
        'STOCK': ["TEST", "TEST", "TEST", "TEST", "TEST", "TEST"],
        'YEAR': pd.Series([2018, 2019, 2020, 2021, 2022, 2023], index=[0, 1, 2, 3, 4, 5], dtype="int64"),
        'AVERAGE_VOLUME': pd.Series([220.6, 120, 300, 200, 350.43, 125.0], index=[0, 1, 2, 3, 4, 5], dtype="float64")
    }, index=[0, 1, 2, 3, 4, 5])

    def test_file_data_is_a_df(self, tmp_path):
        """assert that the file created has a name <CODE>_average_vol_per_year, in csv format,
        with columns STOCK,YEAR,AVERAGE_VOLUME"""
        test_df = TestSaveDataToCsv.test_save_data_df
        stock = Stock("TEST1")
        file_path = os.path.join(tmp_path, 'TEST1_average_vol_per_year.csv')
        stock.save_data_to_csv(test_df, tmp_path)

        # Check that the CSV file was created
        assert os.path.exists(os.path.join(tmp_path, 'TEST1_average_vol_per_year.csv'))

        # Check that the contents of the CSV file match the input DataFrame
        df_loaded = pd.read_csv(file_path)
        pd.testing.assert_frame_equal(test_df, df_loaded)

    def test_file_is_already_existing(self, tmp_path):
        """assert that file will be overwritten if it already exists"""
        # create test file
        existing_file_path = os.path.join(tmp_path, 'TEST2_average_vol_per_year.csv')
        with open(existing_file_path, 'w') as f:
            f.write("Testing, Testing2, Testing3")

        test_df = TestSaveDataToCsv.test_save_data_df
        stock = Stock("TEST2")
        file_path = os.path.join(tmp_path, 'TEST2_average_vol_per_year.csv')
        stock.save_data_to_csv(test_df, tmp_path)

        # Check that the contents of the CSV file match the input DataFrame
        df_loaded = pd.read_csv(file_path)
        pd.testing.assert_frame_equal(test_df, df_loaded)

    def test_path_parameter_is_none(self):
        """assert that file will be written in current working dir"""
        test_df = TestSaveDataToCsv.test_save_data_df
        stock = Stock("TEST3")
        stock.save_data_to_csv(test_df)

        assert os.path.exists(os.path.join(os.getcwd(), 'TEST3_average_vol_per_year.csv'))