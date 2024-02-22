'''
@author Isaiah Terrell-Perica
@date 2/17/24

This file
'''
import os
import logging
from ib_insync import *
import pandas as pd
import numpy as np
import time

from dash_app.logger import log_status

if __name__ == '__main__':
    util.startLoop()
    util.logToConsole(logging.INFO)

    path = '/Users/isaiahtp/Desktop/Zeppelin/z-algo/historical_testing/data'
    duration = "30 D"
    bar_size = "5 secs"
    tickers = pd.read_csv('/Users/isaiahtp/Desktop/Zeppelin/z-algo/nasdaq_screener_1708198817869.csv')
    tickers.sort_values(by='Market Cap', ascending=False, inplace=True)
    try:
        ib = IB()
        ib.connect('127.0.0.1', 7497, clientId=1, timeout=10)

        symbols = tickers['Symbol'][0:100]
        contracts = [Stock(stock, "NYSE", "USD") for stock in symbols]
        qualified = ib.qualifyContracts(*contracts)

        log_status("info", f"Contracts qualified: {len(qualified)}")

        for contract in qualified:
            filename = f"{contract.symbol}_{duration.replace(' ', '')}_{bar_size.replace(' ', '')}.csv"
            if filename in os.listdir(path):
                continue
            log_status("info", f"Requesting data for {contract}")
            bars = ib.reqHistoricalData(
                    contract,
                    endDateTime='',
                    durationStr=duration,
                    barSizeSetting='5 secs',
                    whatToShow='TRADES',
                    useRTH=True,
                    formatDate=1,
                    timeout = 0)
            dataf = util.df(bars)
            dataf.to_csv("data/"+filename, index=False)
            print(f"{filename} saved")
        log_status("info", f"All data done")
    finally:

        ib.disconnect()