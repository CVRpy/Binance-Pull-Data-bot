import binance.client
from binance.client import Client
import api
import pandas as pd
import numpy as np

#PUT YOUR ACCOUNT PKEY AND SKEY:
Pkey = 'SokQ6E89FvlsjySTBDGuR716TumpC9gRGbEnRmQAJE3erxsvrXevpx'
Skey = 'dwOHIxzFCdJPhwzSA3XU6ujkjqUoVYCvXIWcs6g1fLTwEB9cbhqZp'

client = Client(api_key=Pkey, api_secret=Skey)
tickers = ['BTCUSDT'] #YOU CAN CHOOSE ANTHOER COINS
interval = Client.KLINE_INTERVAL_1MINUTE
depth = '1 hours ago'


def pulldata(ticker, interval, depth):

    Cdata = client.get_historical_klines(ticker, interval, depth)
    print(Cdata)
    df = pd.DataFrame(Cdata)
    if not df.empty:

        df[0] = pd.to_datetime(df[0], unit='ms')
        df.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'IGNORE',
                      'Quote_Volume', 'Trades_Count', 'BUY_VOL', 'BUY_VOL_VAL', 'x']
        df = df.set_index('Date')

        del df['IGNORE']
        del df['BUY_VOL']
        del df['BUY_VOL_VAL']
        del df['x']

        df["Open"] = pd.to_numeric(df["Open"])
        df["Open"] = pd.to_numeric(df["Open"])
        df["High"] = pd.to_numeric(df["High"])
        df["Low"] = pd.to_numeric(df["Low"])
        df["Close"] = pd.to_numeric(df["Close"])
        df["Volume"] = round(pd.to_numeric(df["Volume"]))
        df["Quote_Volume"] = round(pd.to_numeric(df["Quote_Volume"]))
        df["Trades_Count"] = pd.to_numeric(df["Trades_Count"])
        df['div'] = df['Open'] / df['Close']

        df['Log_VolumeGain'] = (
            np.log(df["Quote_Volume"]/df.Quote_Volume.shift(1))*100).fillna(0)
        df['pricegain'] = (df.Open.pct_change()*100).fillna(0)

        df.to_csv('/Users/Matrix10/Downloads/Projects/1files/tickers2022.csv')

    print(df)


for ticker in tickers:
    pulldata(ticker, interval, depth)
