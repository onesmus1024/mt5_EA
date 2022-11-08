
import MetaTrader5 as mt5
import pandas as pd
import numpy as np
from mt5_global.settings import symbol, timeframe



# connect to MetaTrader 5
if not mt5.initialize():
    print("initialize() failed, error code =",mt5.last_error())
    quit()

def get_rates(symbol, timeframe, utc_from, utc_to):
    
    # get 10 EURUSD H4 bars starting from 01.10.2020 in UTC time zone
    rates = mt5.copy_rates_range(symbol,timeframe, utc_from, utc_to)
    rates_save = pd.DataFrame(rates)
    rates_save.to_csv("Data/"+symbol+"--"+str(timeframe)+".csv")
    return rates

def get_curr_rates(symbol, timeframe, count):
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, count)
    return rates