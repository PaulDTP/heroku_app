'''
Authored by Isaiah Terrell-Perica
05/31/2023
This file addresses all calculations and data processing needed for images and indicators.
- May need to separate processing for data or conversions
- Should test time taken to run
'''
import os
import time
import datetime
import subprocess

import pandas as pd
import numpy as np
import json
import git
from collections import defaultdict, deque
from dash import dash
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import plotly.express as px

from logger import log_status

max_queue_size = 1000
# X and Y axis data using deque for automatic resizing - check space
btc_timestamps = deque(maxlen=max_queue_size)
btc_prices = defaultdict(lambda: deque(maxlen=max_queue_size))

eth_timestamps = deque(maxlen=max_queue_size)
eth_prices = defaultdict(lambda: deque(maxlen=max_queue_size))
# Dictionary definition
#prices = {'open':[], 'high':[], 'low':[], 'close':[]}

# Gives the last update from git commit
# @return a human readable string of when the last ~/z-algo git commit occurred
def last_updated():
    '''if os.environ.get("LOGNAME") == "isaiahtp":
        # Local path
        repo = git.Repo("~/Desktop/Zeppelin/z-algo").head.commit
    else:
        # Remote path
        repo = git.Repo("~/z-algo").head.commit
    return time.strftime("%a, %d %b %Y %H:%M", time.gmtime(repo.committed_date))'''
    commit_date = subprocess.check_output(['git', 'log', '-1', '--format=%cd'])
    return commit_date.decode('utf-8').strip()

# @return coin data requested by name in the argument
def get_time_price(coin):
    #if coin=='btc':
    if coin==0:
        return btc_timestamps, btc_prices
    #if coin=='eth':
    if coin==1:
        return eth_timestamps, eth_prices

#@return a timestamp converted to a human readable format
def time_conv(timestamp):
    return datetime.datetime.fromtimestamp(timestamp/ 1000).strftime('%Y-%m-%d %H:%M:%S.%f')[:-4]

# Takes data from on_message(ws, message) to process data for the dashboard graph
# @return the graph created from parsing the json response file
def data_processing(message, url):
    log_status('info', 'Data received.')
    data = json.loads(message)

    if 'btc' in url:
        # When receiving kline data:
        timestamp = time_conv(data['E'])
        btc_timestamps.append(timestamp)
        data = data['k']
        btc_prices['open'].append(float(data['o']))
        btc_prices['high'].append(float(data['h']))
        btc_prices['low'].append(float(data['l']))
        btc_prices['close'].append(float(data['c']))
    elif 'eth' in url:
        # When receiving kline data:
        timestamp = time_conv(data['E'])
        eth_timestamps.append(timestamp)
        data = data['k']
        eth_prices['open'].append(float(data['o']))
        eth_prices['high'].append(float(data['h']))
        eth_prices['low'].append(float(data['l']))
        eth_prices['close'].append(float(data['c']))

    # Other data types:
    '''
    #TODO
    '''

# Creates a blank graph ready for data
# @return the initial graph 
def make_graph(title):
    fig = go.Figure()
    fig.add_trace(go.Candlestick())
    fig.update_layout(
        title=title,
        showlegend=False,
        xaxis=dict(
        type="date",
        tickformat="%H:%M:%S %Y-%m-%d"  # Customizing date format
        ),
        yaxis=dict(
            tickformat=".2f", # Precision of y labels
        )
    )
    return fig

# Updates data
def update_data(fig):
    return fig