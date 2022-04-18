# valid intervals - 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M

# get timestamp of earliest date data is available
start_date = client._get_earliest_valid_timestamp('BTCUSDT', '1d')
start_date = to_datetime(start_date)
fmt = "%Y-%m-%d %H:%M:%S"  # e.g. 2019-11-16 23:16:15
# end_date = time.strftime(fmt, time.localtime())
end_date = datetime.now()

def binance_data_to_sql(start_date, end_date, currencytype, timespan, connection):
    cursor = connection.cursor()
    try:
        cursor.execute(f"""create table AlgoModule.{currencytype}_{timespan}
        (
        open_time datetime,
        close_time datetime,
        open_price double,
        close_price double,
        high_price double, 
        low_price double,
        volume double,
        quote_av double,
        trades int,
        tb_base_av double,
        tb_quote_av double
        )""")
        connection.commit()
    except:
        print("Error but moving on")

    step_date = start_date
    while step_date <= end_date:
        print(f'pulling {step_date} data for AlgoModule.{currencytype}_{timespan}')
        bars = client.get_historical_klines(currencytype, timespan, start_str = f'{step_date}', end_str=f'{step_date + timedelta(hours=12)}', limit=1000)
        bars = pd.DataFrame(bars, columns = ['date', 'open',
                    'high', 'low', 'close', 'volume', 'close_time', 'quote_av',
                    'trades', 'tb_base_av', 'tb_quote_av', 'ignore'])
        bars['date'] = bars['date'].apply(to_datetime)
        bars['close_time'] = bars['close_time'].apply(to_datetime)
        for index, row in bars.iterrows():
            cursor.execute(f"""INSERT INTO AlgoModule.{currencytype}_{timespan} (open_time, close_time, open_price, close_price, high_price, low_price,
            volume, quote_av, trades, tb_base_av, tb_quote_av) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
            , (row.date, row.close_time, row.open, row.close, row.high, row.low, row.volume, row.quote_av, row.trades, row.tb_base_av, row.tb_quote_av))
        step_date = step_date + timedelta(hours=12)
        connection.commit()
        sleep(1)


def main():
    currency_pairings = [
        # 'ETHUSD'
     'BTCUSD'
    ]
    time_intervals = [
        '1m' 
        # '3m',
        #  '5m', '15m', '30m', '1h', '2h', '4h', '6h',
        #  '8h', '12h'
        ]
    for cur in currency_pairings:
        for t in time_intervals:
            binance_data_to_sql(start_date, end_date, cur, t, connection)

if __name__ == "__main__":
	main()