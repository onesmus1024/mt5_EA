import MetaTrader5 as mt5
import tensorflow as tf
from tensorflow import keras
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import pandas as pd
from pandas.plotting import scatter_matrix
import numpy as np
import matplotlib.pyplot as plt
import datetime
import pytz
from mt5_global import settings
import time
import os

from mt5_actions.rates import get_rates
from mt5_global.settings import symbol, timeframe


#tset time zone to UTC
timezone = pytz.timezone("Etc/UTC")
utc_from = datetime.datetime(2020, 1, 1, tzinfo=timezone)
utc_to = datetime.datetime.now(tz=timezone)


#get rates from mt5
if settings.Use_local_data:
    rates = pd.read_csv("C:\\Users\\sam\\Desktop\\shared_pro\\mt5_EA\\Data\\EURUSD--15.csv")
else:
    rates = get_rates(symbol,mt5.TIMEFRAME_M15, utc_from, utc_to)

# create DataFrame out of the obtained data
rates_frame = pd.DataFrame(rates)
print(rates_frame.head())

rates_frame.drop(['time'], axis=1)
print(rates_frame.head())
rates_frame.info()
#data visualization and preprocessing  

corretion_matrix =rates_frame.corr()
#time     open     high      low    close  tick_volume  spread  real_volume
#scatter_matrix(rates_frame[attributes],figsize=(12,8))
print(corretion_matrix['close'].sort_values(ascending=False))
x=rates_frame[['open','high','low','tick_volume','spread','real_volume']]
y=rates_frame['close']
#data scaling
scaler = StandardScaler()
scaler.fit(x)
x_scaled = scaler.transform(x)
x = pd.DataFrame(x_scaled, columns=['open','high','low','tick_volume','spread','real_volume'])
x_train_rate,x_test_rate,y_train_rate,y_test_rates = train_test_split(x,y, test_size=0.2)

model = None
history = None
def create_model():
    global model
    global history
    model = keras.Sequential([
        keras.layers.Dense(512,input_shape=[6]),
        keras.layers.Dense(1)
    ])

    model.compile(optimizer='adam',loss='mse',metrics=['mae'])

    history = model.fit(x_train_rate,y_train_rate,epochs=100,validation_split=0.2,batch_size=50)
    root_dir = os.path.join(os.curdir,"models/saved_models")
    def get_run_logdir():
        run_id =symbol+"-"+time.strftime("run_%Y_%m_%d-%H_%M_%S")
        return run_id
    #save model
    model.save(os.path.join(root_dir,get_run_logdir()))

def plot_learning_curves(history):
    plt.plot(history.history['loss'],label='loss',color='red')
    plt.plot(history.history['val_loss'],label='val_loss',color='blue')
    plt.legend()
    #plt.gca().set_ylim(0,0.001)
    plt.show()
    score = model.evaluate(x_test_rate,y_test_rates)
    print(score)
if not settings.Use_saved_model:
    create_model()
if settings.Debug and not settings.Use_saved_model:
    plot_learning_curves(history)
  




