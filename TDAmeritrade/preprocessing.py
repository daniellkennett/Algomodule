"""
Author: Daniel Kennett

Functions for preprocessing data
"""
from src.TechAnalysis import TechAnalysis
from datetime import datetime
import numpy as np

def time_processing(df):
    """
    Time function for TDA data
    """
    dt = np.array(df['datetime'].values)/1000
    func = lambda x: datetime.fromtimestamp(x)
    funcvec = np.vectorize(func)
    dt = funcvec(dt)
    return dt

def preprocessing(df, price_offset = 1.000001, prediction = False, best_d_value = 1, len_of_original_weights = 64):
    column_name = 'close'
    ta = TechAnalysis(df)
    """
    Imputes fractional differencing into data
    """
    if prediction:
        df = df[(len(df) - (len_of_original_weights+1)):]
        df_fd, weights = ta.frac_diff(df[column_name], best_d_value)        
    else:
        
        df_fd, weights, best_d_value = ta.fractional_difference(column_name, alpha=.05)
       
    df['datetime'] = time_processing(df)    
    df['frac_diff_cost'] = np.nan
    df['frac_diff_cost'].iloc[len(weights):] = df_fd[0]

    """
    Create mass features
    """
    steps = [5, 10, 20, 30, 40, 50]
    macds = [[2,10],[5,10],[10,20],[10,30],[20,30]]
    bbs_std = [1, 1.5, 2]

    for step in steps:
        df[f'ma_{step}'] = ta.moving_average(column_name, step)
        df[f'ewa_{step}'] = ta.moving_average(column_name, step, simple=False)
        df[f'rsi_{step}'] = ta.rsi(column_name, step)
        for std in bbs_std:
            df[f'bb_{step}_{std}_upper'],  df[f'bb_{step}_{std}_lower']= ta.bollinger_bands(column_name, step, std = std)


    for macd in macds:
        short, long = macd
        df[f'rsi_{step}'] = ta.macd(column_name, short, long)

    if not prediction:
        df['target_classifier'] = 0
        df['target_classifier'][df['target']>df['close']*price_offset] = 1
        df.reset_index(inplace=True, drop=True)
        df.drop(['target'], axis=1, inplace=True)
        
    df.drop(['datetime', 'open', 'high', 'low'], axis=1, inplace=True)
    df.dropna(inplace=True)
    
    return df, best_d_value, weights