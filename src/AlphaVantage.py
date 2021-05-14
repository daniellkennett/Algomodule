import pandas as pd
import numpy as np
import requests
import time

def currency_rate(cur1, cur2, api = 'OZHBQ2Q48QC0NFRZ'):
    rate = requests.get(f'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={cur1}&to_currency={cur2}&apikey={api}').json()
    rate = rate['Realtime Currency Exchange Rate']
    return pd.DataFrame([rate.values()], columns=rate.keys())


def continuous_rate(cur1, cur2, seconds = 15):
    data = currency_rate(cur1, cur2)
    while True:
        time.sleep(seconds)
        data_next = currency_rate(cur1, cur2)
        data = data.append(data_next)
        data.to_csv('../data/time_series_data.csv')
        
if __name__ == '__main__':        
    print(continuous_rate('EUR','USD'))