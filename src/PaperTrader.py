from datetime import datetime
import numpy as np
class PaperTrader():
    """
    Author: Daniel Kennett
    
    The intent of this class is to simulate paper trading. It will track buying positions, as well as return the sale as well.
    Will only sell what is bought
    """
    free_cash = 0
    key = 0
    record = {'key': [], 'ticker': [], 'buy_price': [], 'buy_amount': [], 'buy_total_amount': [], 'buy_time': [], 
              'sell_price':[], 'sell_amount': [], 'sell_total_amount': [], 'sell_time': [], 'open': [], 'profit/loss':[]}
    
    def __init__(self, starting_amount):
        self.free_cash = starting_amount
        
    def now():
        return datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        
    def current_free_cash(self):
        return self.free_cash
    
    def current_record(self):
        return self.record
    
    def buy(self, ticker, buy_price, buy_amount):
        total = buy_price*buy_amount
        self.free_cash -= total
        
        self.record['key'].append(self.key)
        self.record['ticker'].append(ticker)
        self.record['buy_price'].append(buy_price)
        self.record['buy_amount'].append(buy_amount)
        self.record['buy_total_amount'].append(total)
        self.record['buy_time'].append(PaperTrader.now())

        self.record['sell_price'].append(np.nan)
        self.record['sell_amount'].append(np.nan)
        self.record['sell_total_amount'].append(np.nan)
        self.record['sell_time'].append(PaperTrader.now())
        self.record['open'].append(True)
        self.record['profit/loss'].append(np.nan)
        self.key+=1
        return self.key-1
        
    def sell(self, key, sell_price, sell_amount):
        total = sell_price * sell_amount
        self.free_cash += total
        
        i = self.record['key'].index(key)
        self.record['sell_price'][i] = sell_price
        self.record['sell_amount'][i] = sell_amount
        self.record['sell_total_amount'][i] = total
        self.record['sell_time'][i] = PaperTrader.now()
        self.record['open'][i] = False
        self.record['profit/loss'][i] = total - self.record['buy_total_amount'][i]