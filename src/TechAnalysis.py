from statsmodels.tsa.stattools import adfuller
import numpy as np
import pandas as pd

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
    
    
    """
    Use Fractional Differencing to create stationary data for predictions
    Data offsets by weights_window_size
    """
    
    @staticmethod
    def get_weights_floored(d, num_k, floor=1e-3):
        r"""Calculate weights ($w$) for each lag ($k$) through
        $w_k = -w_{k-1} \frac{d - k + 1}{k}$ provided weight above a minimum value
        (floor) for the weights to prevent computation of weights for the entire
        time series.

        Args:
            d (int): differencing value.
            num_k (int): number of lags (typically length of timeseries) to calculate w.
            floor (float): minimum value for the weights for computational efficiency.
        """
        w_k = np.array([1])
        k = 1

        while k < num_k:
            w_k_latest = -w_k[-1] * ((d - k + 1)) / k
            if abs(w_k_latest) <= floor:
                break

            w_k = np.append(w_k, w_k_latest)

            k += 1

        w_k = w_k.reshape(-1, 1) 

        return w_k
    
    @staticmethod
    def frac_diff(df, d, floor=1e-3):
        r"""Fractionally difference time series via CPU.

        Args:
            df (pd.DataFrame): dataframe of raw time series values.
            d (float): differencing value from 0 to 1 where > 1 has no FD.
            floor (float): minimum value of weights, ignoring anything smaller.
        """
        # Get weights window
        weights = TechAnalysis.get_weights_floored(d=d, num_k=len(df), floor=floor)
        weights_window_size = len(weights)

        # Reverse weights
        weights = weights[::-1]

        # Blank fractionally differenced series to be filled
        df_fd = []

        # Slide window of time series, to calculated fractionally differenced values
        # per window
        for idx in range(weights_window_size, df.shape[0]):
            # Dot product of weights and original values
            # to get fractionally differenced values
            date_idx = df.index[idx]
            df_fd.append(np.dot(weights.T, df.iloc[idx - weights_window_size:idx]).item())

        # Return FD values and weights
        df_fd = pd.DataFrame(df_fd)

        return df_fd, weights

    def fractional_difference(self, column_name, alpha):
        """
        Run iterations of fractional differing to find best d_value.
        Do this by running adfuller test. A test of Stationarity. Low p_value = Stationarity
        Returns values, weights, and d_value of best_d_value
        """
        adfs = []

        for d in np.linspace(0,1,51):
            df_fd, weights = TechAnalysis.frac_diff(self.df[column_name], d)
            pvalue = adfuller(df_fd.values)[1]
            adfs.append([d, pvalue])
            if pvalue < alpha:
                break      
        best_d_value = adfs[-1][0]
        
        
        return df_fd, weights, best_d_value