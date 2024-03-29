import binance.client
from binance.client import Client
import api
import pandas as pd
import numpy as np

#PUT YOUR ACCOUNT PKEY AND SKEY:
Pkey = ''
Skey = ''
#######################################
client = Client(api_key=Pkey, api_secret=Skey)
client = Client()
tickers = ['BTCUSDT'] #YOU CAN CHOOSE ANTHOER COINS
interval = Client.KLINE_INTERVAL_1MINUTE
depth = '1 hours ago'
########################################

def data(ticker, interval, depth):

    Bdata = client.get_historical_klines(ticker, interval, depth)
    df = pd.DataFrame(Bdata)
    
    if not df.empty:
        df[0] = pd.to_datetime(df[0], unit='ms')
        df.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'IGNORE',
                      'Quote_Volume', 'Trades_Count', 'BUY_VOL', 'BUY_VOL_VAL', 'y']
        df = df.set_index('Date')

        df["Open"] = pd.to_numeric(df["Open"])
        df["Open"] = pd.to_numeric(df["Open"])
        df["High"] = pd.to_numeric(df["High"])
        df["Low"] = pd.to_numeric(df["Low"])
        df["Close"] = pd.to_numeric(df["Close"])
        df["Volume"] = round(pd.to_numeric(df["Volume"]))
        df["Quote_Volume"] = round(pd.to_numeric(df["Quote_Volume"]))
        df["Trades_Count"] = pd.to_numeric(df["Trades_Count"])
        df['Log_VolumeGain'] = (
            np.log(df["Quote_Volume"]/df.Quote_Volume.shift(1))*100).fillna(0)
        df['pricegain'] = (df.Open.pct_change()*100).fillna(0)

        df.to_csv('/Users/Matrix10/Downloads/Projects/1files/tickers2022.csv')

    print(df)
    return df


for ticker in tickers:
    data(ticker, interval, depth)
