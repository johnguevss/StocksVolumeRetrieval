from stock import Stock

if __name__ == '__main__':
    tsla = Stock("TSLA")
    weekly_tsla = tsla.get_weekly_stock_data()
    print(weekly_tsla)
    if weekly_tsla:
        clean_data = tsla.clean_stock_data(weekly_tsla)
        print(clean_data.head())
        vol_by_year = tsla.compute_avg_volume(clean_data, 5)
        tsla.save_data_to_csv(vol_by_year)
