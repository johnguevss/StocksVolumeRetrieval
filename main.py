from stock import Stock

if __name__ == '__main__':
    tsla = Stock("TSLA")
    weekly_tsla = tsla.get_weekly_stock_data()

    if weekly_tsla:
        clean_data = tsla.clean_stock_data(weekly_tsla)
        vol_by_year = tsla.compute_avg_volume(clean_data)
        tsla.save_data_to_csv(vol_by_year)
