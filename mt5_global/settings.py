import MetaTrader5 as mt5
import datetime
import pytz

timezone = pytz.timezone("Etc/UTC")
Model_type = "v1_ANN"
symbol = "EURUSD"
timeframe = mt5.TIMEFRAME_M15
time_series = 1 #number of time series to be used for prediction
Debug = False
Use_local_data = False
Use_saved_model = False

utc_from = datetime.datetime(2020, 3, 1, tzinfo=timezone)