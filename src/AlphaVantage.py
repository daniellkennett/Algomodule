import pandas as pd
import numpy as np
import requests
import time

def currency_rate(cur1='USD', cur2='EUR', api_key = 'OZHBQ2Q48QC0NFRZ'):
    rate = requests.get(f'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={cur1}&to_currency={cur2}&apikey={api_key}').json()
    rate = rate['Realtime Currency Exchange Rate']
    return pd.DataFrame([rate.values()], columns=rate.keys())


def continuous_rate(cur1='USD', cur2='EUR', seconds = 15):
    data = currency_rate(cur1, cur2)
    while True:
        time.sleep(seconds)
        data_next = currency_rate(cur1, cur2)
        data = data.append(data_next)
        data.to_csv('../data/time_series_data.csv')
        
def historic_rate(cur1='USD', cur2='EUR', interval = '5min', api_key = 'OZHBQ2Q48QC0NFRZ'):
    rate = requests.get(f"https://www.alphavantage.co/query?function=FX_INTRADAY&from_symbol={cur1}&to_symbol={cur2}&interval={interval}&apikey={api_key}").json()
    rate = rate['Time Series FX (5min)']
    return pd.DataFrame(rate).T
    
def continuous_historic_rate(cur1='USD', cur2='EUR',seconds = 300):
    data = historic_rate(cur1,cur2)
    data.to_csv('../data/historic_time_series_data.csv')
    while True:
        time.sleep(seconds)
        data_next = historic_rate(cur1,cur2).iloc[-1]
        data = data.append(data_next)
        data.to_csv('../data/historic_time_series_data.csv')
        
if __name__ == '__main__':        
    print(continuous_historic_rate('EUR','USD'))
