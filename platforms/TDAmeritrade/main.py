"""
Compile code into one file to check data and file trades

"""
import sys
sys.path.append('../')
from config.tda.config import JSON_PATH, CONSUMER_KEY, REDIRECT_URI, WEBDRIVER, tda_login

import pandas as pd
from preprocessing import time_processing, preprocessing


stock_ticker = 'VOO'

data = pd.DataFrame(c.get_price_history_every_minute(stock_ticker).json()['candles'])
data['target'] = data['close'].shift(-1)
data, best_d_value, weights = preprocessing(data, price_offset = 1.000001)