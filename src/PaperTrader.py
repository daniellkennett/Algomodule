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
    record = {}
    
    def __init__(self, starting_amount):
        self.free_cash = starting_amount
        self.record = {'key': [], 'ticker': [], 'coin_buy_price': [], 'coin_buy_amount': [], 'usd_buy_total_amount': [], 'buy_time': [], 'usd_buy_fee': [], 'coin_buy_fee':[], 'usd_buy_amount_after_fee':[], 'coin_buy_amount_after_fee':[],
              'coin_sell_price':[], 'coin_sell_amount': [], 'usd_sell_total_amount': [], 'sell_time': [], 'usd_sell_fee': [], 'coin_sell_fee': [], 'usd_sell_amount_after_fee':[], 'coin_sell_amount_after_fee':[], 
              'open': [], 'profit/loss':[], 'free_cash':[]}
        
    def now():
        return datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        
    def current_free_cash(self):
        return self.free_cash
    
    def current_record(self):
        return self.record
    
    def buy(self, ticker, buy_price, buy_amount, buyer_fee = 0):
        total = buy_price*buy_amount
        fee = buy_price*buy_amount*buyer_fee
        total_wfee = total-fee
        
        self.record['key'].append(self.key)
        self.record['ticker'].append(ticker)
        self.record['coin_buy_price'].append(buy_price)
        self.record['coin_buy_amount'].append(buy_amount)
        self.record['usd_buy_total_amount'].append(total)
        self.record['buy_time'].append(PaperTrader.now())
        self.record['usd_buy_fee'].append(fee)
        self.record['coin_buy_fee'].append(buyer_fee*buy_amount)
        self.record['usd_buy_amount_after_fee'].append(total_wfee)
        self.record['coin_buy_amount_after_fee'].append((1-buyer_fee)*buy_amount)

        self.record['coin_sell_price'].append(np.nan)
        self.record['coin_sell_amount'].append(np.nan)
        self.record['usd_sell_total_amount'].append(np.nan)
        self.record['sell_time'].append(PaperTrader.now())
        self.record['usd_sell_fee'].append(np.nan)
        self.record['coin_sell_fee'].append(np.nan)
        self.record['usd_sell_amount_after_fee'].append(np.nan)
        self.record['coin_sell_amount_after_fee'].append(np.nan)

        self.record['open'].append(True)
        self.record['profit/loss'].append(np.nan)
        self.record['free_cash'].append(np.nan)

        self.free_cash -= fee
        self.free_cash -= total
        self.key+=1
        return self.key-1
        
    def sell(self, key, sell_price, sell_amount, seller_fee = 0):
        total = sell_price * sell_amount 
        fee = sell_price*sell_amount*seller_fee
        total_wfee = total-fee

        i = self.record['key'].index(key)
        self.record['coin_sell_price'][i] = sell_price
        self.record['coin_sell_amount'][i] = sell_amount
        self.record['usd_sell_total_amount'][i] = total
        self.record['sell_time'][i] = PaperTrader.now()

        self.record['usd_sell_fee'][i] = fee
        self.record['coin_sell_fee'][i] = (sell_amount*seller_fee)
        self.record['usd_sell_amount_after_fee'][i] = total_wfee
        self.record['coin_sell_amount_after_fee'][i] = sell_amount * (1-seller_fee)

        self.free_cash += total_wfee
        self.record['open'][i] = False
        self.record['profit/loss'][i] = total_wfee - self.record['usd_sell_amount_after_fee'][i]
        self.record['free_cash'][i] = self.free_cash