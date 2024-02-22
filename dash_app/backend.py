'''
@author Isaiah Terrell-Perica
@date 05/31/2023

This file handles all calculations and data processing needed for coin graphs and technical indicators.

- May need to separate processing for data or conversions
- Should test time taken to run functions
'''
from datetime import datetime
import subprocess

import dash
import pandas as pd
import numpy as np
import json
import git
from collections import defaultdict, deque
from dash.dependencies import Input, Output
import plotly.graph_objs as go

from dash_app.logger import log_status, get_logs

def last_updated():
    """
    Returns the last update from git commit
    :return: human-readable string of last ~/z-algo git commit
    """
    commit_date = subprocess.check_output(['git', 'log', '-1', '--format=%cd'])
    return commit_date.decode('utf-8').strip()


def make_graph(title):
    """
    Creates a blank graph ready for data
    :param title: title for created graph
    :return fig: blank Figure object
    """
    fig = go.Figure()
    # fig.add_trace(go.Candlestick(name='main'))
    fig.add_trace(go.Scatter(name='main', mode='lines'))
    fig.update_layout(
        title=title,
        showlegend=False,
        xaxis=dict(
            type="date",
            tickformat="%H:%M:%S" #%Y-%m-%d"  # Customizing date format
        ),
        yaxis=dict(
            tickformat=".2f",  # Precision of y labels
        ),
        uirevision=True # maintains user state
    )
    return fig

def time_conv(timestamp):
    """
    Converts timestamp to a human-readable format
    :param timestamp: epoch time to convert
    :return: human-readable time
    """
    return datetime.fromtimestamp(timestamp / 1000).strftime('%Y-%m-%d %H:%M:%S')


# Eventually this should be its own background worker:
# - pull data from Postgresql database
# - categorize data and do calculations
# - push data to next process to populate the graph
def data_processing(trades):
    sec_data = {}
    for data in trades:
        symbol = data['symbol']  # Symbol (ex: BNBBTC)
        event = data['info']['e']  # Event type (kline, aggtrade, etc)
        timestamp = time_conv(data['timestamp'])  # Event time ex: 1672515782136

        sec_data[timestamp] = data['price']
    if len(sec_data) > 1:
        log_status("error", "Processing funct. larger than 1")
    return sec_data

def json_data_processing(trades):
    """
    JSON Loads:
    {'e': 'trade',
     'E': 1708580838879,
     's': 'BTCUSDT',
     't': 1168941,
     'p': '51573.88000000',
     'q': '0.00010000',
     'b': 5630322,
     'a': 5630360,
     'T': 1708580838878,
     'm': True,
     'M': True}
    :param trades: trades to parse
    :return sec_data: dict with key time and value price
    """
    sec_data = {}
    data = json.loads(trades['data'])

    symbol = data['s']  # Symbol (ex: BNBBTC)
    event = data['e']  # Event type (kline, aggtrade, etc)
    timestamp = time_conv(data['E'])  # Event time ex: 1672515782136

    sec_data[timestamp] = data['p']
    if len(sec_data) > 1:
        log_status("error", "Processing funct. returning larger than 1")
    return sec_data

# Payload Types
'''
Trade Stream Payload
Update Speed: Real-time
{
  "e": "trade",     // Event type
  "E": 1672515782136,   // Event time
  "s": "BNBBTC",    // Symbol
  "t": 12345,       // Trade ID
  "p": "0.001",     // Price
  "q": "100",       // Quantity
  "b": 88,          // Buyer order ID
  "a": 50,          // Seller order ID
  "T": 1672515782136,   // Trade time
  "m": true,        // Is the buyer the market maker?
  "M": true         // Ignore
}

Candlesticks
Update Speed: 2000ms
{
  "e": "kline",     // Event type
  "E": 1672515782136,   // Event time
  "s": "BNBBTC",    // Symbol
  "k": {
    "t": 1672515780000, // Kline start time
    "T": 1672515839999, // Kline close time
    "s": "BNBBTC",  // Symbol
    "i": "1m",      // Interval
    "f": 100,       // First trade ID
    "L": 200,       // Last trade ID
    "o": "0.0010",  // Open price
    "c": "0.0020",  // Close price
    "h": "0.0025",  // High price
    "l": "0.0015",  // Low price
    "v": "1000",    // Base asset volume
    "n": 100,       // Number of trades
    "x": false,     // Is this kline closed?
    "q": "1.0000",  // Quote asset volume
    "V": "500",     // Taker buy base asset volume
    "Q": "0.500",   // Taker buy quote asset volume
    "B": "123456"   // Ignore
  }
}
24h Change 
Update Speed: 1000ms
{
  "e": "24hrTicker",  // Event type
  "E": 1672515782136,     // Event time
  "s": "BNBBTC",      // Symbol
  "p": "0.0015",      // Price change
  "P": "250.00",      // Price change percent
  "w": "0.0018",      // Weighted average price
  "x": "0.0009",      // First trade(F)-1 price (first trade before the 24hr rolling window)
  "c": "0.0025",      // Last price
  "Q": "10",          // Last quantity
  "b": "0.0024",      // Best bid price
  "B": "10",          // Best bid quantity
  "a": "0.0026",      // Best ask price
  "A": "100",         // Best ask quantity
  "o": "0.0010",      // Open price
  "h": "0.0025",      // High price
  "l": "0.0010",      // Low price
  "v": "10000",       // Total traded base asset volume
  "q": "18",          // Total traded quote asset volume
  "O": 0,             // Statistics open time
  "C": 1675216573749,      // Statistics close time
  "F": 0,             // First trade ID
  "L": 18150,         // Last trade Id
  "n": 18151          // Total number of trades
}

'''