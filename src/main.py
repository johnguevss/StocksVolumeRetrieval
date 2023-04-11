from stock import Stock
import sys

try:
    LAST_N_YEARS = int(sys.argv[2])
except IndexError as e:
    LAST_N_YEARS = 5
finally:
    CHOSEN_STOCK = sys.argv[1]
    if __name__ == '__main__':
        stock = Stock(CHOSEN_STOCK)
        weekly_tsla = stock.get_weekly_stock_data()

        if weekly_tsla:
            clean_data = stock.clean_stock_data(weekly_tsla)
            print(clean_data.head())
            vol_by_year = stock.compute_avg_volume(clean_data, LAST_N_YEARS)
            stock.save_data_to_csv(vol_by_year)
