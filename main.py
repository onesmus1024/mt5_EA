from operator import mod
import numpy as np
import pandas as pd
from tensorflow import keras
import datetime
import time
import pytz
import MetaTrader5 as mt5
from models.model import model
from mt5_global import settings
from mt5_actions.authorize import login
from mt5_actions.tick import get_curr_ticks
from mt5_actions.rates import get_curr_rates
from mt5_actions.order import buy_order, sell_order
from mt5_global.settings import symbol, timeframe
from models.model import scaler


saved_model = None


# order parameters
lot = 0.1
point = mt5.symbol_info(symbol).point
if settings.Use_saved_model:
    # keras.mode
    my_model = keras.models.load_model("models/saved_models/EURUSD-run_2022_11_04-18_32_24")
else:
    my_model = model

def trade():
    if not login():
        print('login failed')
        return
    rates = get_curr_rates(symbol,timeframe, 1)
    while True:
        try:
            curr_rate =get_curr_rates(symbol,timeframe, 1)
            curr_rate_frame = pd.DataFrame(curr_rate)
            previous_rates_frame = pd.DataFrame(rates)
            if int(curr_rate_frame['time'])== int(previous_rates_frame['time']):
                time.sleep(2)
                continue

            #drop time column
            previous_rates_frame=previous_rates_frame.drop(['time','close'], axis=1)
        
            #scale data
            x_scaled = scaler.transform(previous_rates_frame)
            x = pd.DataFrame(x_scaled, columns=['open','high','low','tick_volume','spread','real_volume'])
            #predict
            prediction = my_model.predict(x)
            prediction = round(prediction[0][0],5)
            #get current price
            curr_price = mt5.symbol_info_tick(symbol).ask

            if prediction > curr_price:
                buy_order(prediction,symbol)
            elif prediction < curr_price:
                sell_order(prediction,symbol)
            else:
                print('no action')
        except Exception as e:
            print(e)
            print("order failed")
            login()
            time.sleep(2)

            rates = get_curr_rates(symbol,timeframe, 1)
            pass
        rates = get_curr_rates(symbol,timeframe, 1)



if __name__ == "__main__":
    trade()
   
       

