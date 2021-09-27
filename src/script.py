import pandas as pd
import talib
import requests
from time import sleep
import yfinance as yf
from bs4 import BeautifulSoup
import numpy as np
from datetime import datetime
import re
dt = datetime.today()

url = 'https://finance.yahoo.com/quote/EURUSD=X?p=EURUSD=X&.tsrc=fin-srch'
headers = {'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
            'referer' : 'https://www.google.com/'}


def get_price(url, headers):
    bid_class = "Ta(end) Fw(600) Lh(14px)"
    ask_class = "Ta(end) Fw(600) Lh(14px)"
    time_class = "C($tertiaryColor) D(b) Fz(12px) Fw(n) Mstart(0)--mobpsm Mt(6px)--mobpsm"


    d = {'bid': [],
         'ask': [],
         'time': []}
    
    bb = requests.get(url, headers=headers)
    soup = BeautifulSoup(bb.content.decode(), 'html.parser')

    mydivs = soup.find_all("td", {"class": bid_class})
    bid = mydivs[2].find('span')
    ask = mydivs[5].find('span')
    d['bid'].append(bid.text)
    d['ask'].append(ask.text)


    mytime = soup.find_all("div", {"class": time_class})
    time_ = mytime[0].find('span').get_text()
    time_re = re.findall(r'\d{1,2}(?:(?:AM|PM)|(?::\d{1,2})(?:AM|PM)?)', time_)

    d['time'].append(time_re[0])

    df = pd.DataFrame(d)
    return df

def continuous(time=60):
    df = get_price(url, headers)
    trigger = True
    while trigger:
        sleep(time)
        try:
            dt = datetime.today()
            df = df.append(get_price(url, headers))
            df.to_csv(f'../data/EURUSD/EURUSD=X{dt.month}-{dt.day}-{dt.year}.csv')
        except:
            pass
            print('failure')
            
        
if __name__ == '__main__':        
    continuous(60)
