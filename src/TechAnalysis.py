class TechAnalysis:
    """
    A class to run Technical Analysis on a Pandas Dataframe
    
    """
    def __init__(self, df):
        self.df = df

    def moving_average(self, column_name, steps, simple=True):
        ##5,10,30,60steps##
        if simple:
            ma = self.df[column_name].rolling(steps).mean()
        else:
            ma = self.df[column_name].ewm(com=.5).mean()
        return ma
        
    def rsi(self, column_name, steps):
        # 5,10,30,60 steps#
        diff_inc = self.df[column_name].diff()
        diff_dec = diff_inc.copy(deep=True)
        diff_inc[diff_inc<0] = 0
        diff_dec[diff_dec>=0] = 0
        diff_dec *= -1
        inc = diff_inc.rolling(steps).mean()
        dec = diff_dec.rolling(steps).mean()
        
        rsi = inc/dec
        rsi = 100 - (100/(1+rsi))
        return rsi
        
    def macd(self, column_name, short_step, long_step, simple=True):
        #[10,30], [5,10],[2,10] #
        #simple moving average vs exponential moving average#
        if simple:
            short = self.moving_average(column_name, short_step, simple=True)
            long = self.moving_average(column_name,  long_step, simple=True)
        else:
            short = self.moving_average(column_name, short_step, simple=False)
            long = self.moving_average(column_name, long_step, simple=False)
        
        macd = long-short
        
        return macd
        
    def bollinger_bands(self, column_name, steps, std=1.5, simple=True):
        #[10,1.5], [20, 2], [50, 2.5] #
        if simple:
            ma = self.moving_average(column_name, steps, simple=True)
        else: 
            ma = self.moving_average(column_name, steps, simple=False)
            
        sigma = self.df[column_name].rolling(steps).std()
        
        upper = ma + (std*sigma)
        lower = ma - (std*sigma)
        return upper, lower
    def fib_retracement(self, column_name, days, fib=1):
        #23.6%, 38.2%, 50%, 61.8%, and 100%#
        return None