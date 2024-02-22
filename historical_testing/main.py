"""
@author: Isaiah Terrell-Perica
@date: 02/09/2024

This file handles backtesting of different strategies and their outputs.
"""

import os
import pandas as pd
import numpy as np
import multiprocessing
from datetime import datetime
import concurrent.futures

from dash_app.logger import log_status
import logging
from backtesting import Backtest, Strategy

index_set = False
lock = multiprocessing.Lock()

hits1 = 0
hits2 = 0
hits3 = 0
hits4 = 0

class Zeppelin(Strategy):
    # If you extend composable strategies from `backtesting.lib`,
    # make sure to call super().init() and super().next()
    def init(self):
        """
        Initialize the strategy.
        Declare indicators (with `backtesting.backtesting.Strategy.I`).
        Precompute what needs to be precomputed or can be precomputed
        in a vectorized fashion before the strategy starts.
        ALL DATA IS AVAILABLE IN HERE
        """
        # super().init()
        self.open = self.data["Open"][0]
        self.dropped = False
        self.dropped_price = 0
        self.dropped_up20 = False
        # In Live Trading you'd want to have this set from the open time on the first data point
        self.rolling2m = {'price': self.open, 'time': self.data.index[0]}
        self.rolling1m = {'price': self.open, 'time': self.data.index[0]}
        self.rolling1d = {'price': self.open, 'time': self.data.index[0]}

        # self.hits1 = 0
        # self.hits2 = 0
        # self.hits3 = 0
        # self.hits4 = 0

    def next(self):
        """
        Main strategy runtime method, called as each new
        `backtesting.backtesting.Strategy.data`
        instance (row; full candlestick bar) becomes available.
        This is the main method where strategy decisions -
        upon data precomputed in `backtesting.backtesting.Strategy.init` -
        take place.
        """
        # super().next()
        # price = (self.data.Close[-1] - self.data.Open[-1]) / 2 # midpoint price
        price = self.data.Close[-1]
        time = self.data.index[-1]
        global hits1, hits2, hits3, hits4

        # These pct changes are calculated on Open column
        pct_change1m = self.data['Pct Change 1m'][-1]
        pct_change2m = self.data['Pct Change 2m'][-1]

        rolling1m = (price - self.rolling1m['price']) / self.rolling1m['price']
        rolling2m = (price - self.rolling2m['price']) / self.rolling2m['price']
        rolling1d = (price - self.rolling1d['price']) / self.rolling1d['price']

        # If n minutes have elapsed, reset the indicator
        if (time - self.rolling2m['time']).total_seconds() > 120:
            self.rolling2m['price'] = price
            self.rolling2m['time'] = time
        if (time - self.rolling1m['time']).total_seconds() > 60:
            self.rolling1m['price'] = price
            self.rolling1m['time'] = time
        if (time - self.rolling1d['time']).days > 0:
            self.rolling1m['price'] = price
            self.rolling1m['time'] = time

        time = self.data.index[-1].hour * 60 + self.data.index[-1].minute

        # If the stock drops from between 0.5% and 0.9% in one minute, buy and sell at a 0.25% gain
        if 0.005 < rolling1m < 0.009:
            hits1 += 1
            self.buy(size=1, tp=price*1.0025)

        # If the stock drops 2% in 2 minutes or less buy and place a sell order for 1.2% above
        if rolling2m <= -0.02:
            #if pct_change2m >= 0.02 or pct_change1m >= 0.02:
            hits2 += 1
            self.buy(size = 1, tp=price*1.012)

        # If DOW drops 1.2% or more in the first 90 mins of the day, buy and sell for 0.6% gain
        if time < (11*60+1):
            if rolling1d >= 0.012:
                hits3 += 1
                self.buy(size = 1, tp=price*1.006)

        # If the Dow drops 175 points (0.006) or more from Open and then goes up more than 20 (0.00067) points and
        # returns to within 15 (0.0005) points of that low, buy and sell for a 50 (0.0017) point gain
        if rolling1d <= -0.006: # dropped 175 points from Open
            self.dropped = True
            self.dropped_price = price # setting to price dropped to
        if self.dropped: # price has dropped 175+ points from Open
            if not self.dropped_up20 and (price - self.dropped_price)/self.dropped_price >= 0.00067: # price has gone up .00067% points
                self.dropped_up20 = True
            if self.dropped_up20:
                if price*.9995 < self.dropped_price < price*1.0005:
                    hits4 += 1
                    self.buy(size=1, tp=price*1.003)

def market_hours(date):
    return 9 * 60 + 30 <= date.hour * 60 + date.minute <= 16 * 60 + 1
def load_data(file):
    """
    Loads data file and applies organization
    :return dia: parsed security as a DataFrame
    """
    # path = '/Users/isaiahtp/Desktop/freqtrade/user_data/data/1m_data/'
    path = "data/"
    symbol = file
    dia = pd.read_csv(path + symbol, parse_dates=[0], date_format='%Y-%m-%d %H:%M:%S%z') # read data and provide date format
    dia.columns = map(str.capitalize, dia.columns) # capitlize columns
    dia['Date'] = dia['Date'].dt.tz_convert('America/New_York').dt.tz_localize(None) # remove timezone info
    dia.set_index('Date', inplace=True)
    dia['Pct Change 1m'] = dia['Close'].pct_change(freq=pd.DateOffset(minutes=1))
    dia['Pct Change 2m'] = dia['Close'].pct_change(freq=pd.DateOffset(minutes=2))
    #new_columns = {'Hits 1': 0, 'Hits 2': 0, 'Hits 3': 0, 'Hits 4': 0}
    #dia = dia.assign(**new_columns)
    return dia

def bootstrap(data, drop_na=False):
    if drop_na:
        booted = data.dropna().sample(len(data), replace=True, ignore_index = True)
    else:
        booted = data.sample(len(data), replace=True, ignore_index = True)
    return booted

def run_backtest(strategy, data):
    name = data.split("_")[0]
    # for graphs in os.listdir('/Users/isaiahtp/Desktop/Zeppelin/z-algo/historical_testing/graphs'):
    #     if f"{name}.html" in graphs:
    #         return
    global index_set

    bt = Backtest(load_data(data), Zeppelin, cash=100000, commission=0.002, trade_on_close=False, hedging=True)
    msg = bt.run()
    ticker_col = pd.Series(msg)
    print(f"Stats for {name}:")
    print(hits1, hits2, hits3, hits4)
    print(ticker_col)

    bt.plot(resample=False, open_browser=False, filename=f"graphs/{name}")
    try:
        pass
        # sql shit
    except Exception as e:
        log_status("info", f"Problem with {name}:\n{e}")
    return pd.DataFrame(index=[name], data=[ticker_col.values], columns=[ticker_col.index])

if __name__ == "__main__":
    all_tickers = pd.DataFrame()
    files = []
    for file in os.listdir('/Users/isaiahtp/Desktop/Zeppelin/z-algo/historical_testing/data'):
        if "30D" in file:
            files.append(file)
    num_workers = multiprocessing.cpu_count()
    with concurrent.futures.ProcessPoolExecutor() as executor:
        # Use submit to asynchronously execute the run_backtest function for each dataset
        futures = [executor.submit(run_backtest, Zeppelin, data) for data in files]
        # Wait for all futures to complete
        concurrent.futures.wait(futures)
        # Retrieve results
        results = [future.result() for future in futures]
    # Process the results as needed
    all_tickers = pd.concat(results, axis=1)
    #all_tickers = all_tickers.
    # make sure the axes are correct and
    all_tickers.to_csv("btdata0_100.csv", index=True)