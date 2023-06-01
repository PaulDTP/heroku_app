import time
import datetime

import pandas as pd
import numpy as np
import json
import git
from collections import defaultdict, deque

from dash.dependencies import Input, Output
import plotly.graph_objs as go
import plotly.express as px

max_queue_size = 10
# x and y data
timestamps = deque(maxlen=max_queue_size)
prices = defaultdict(lambda: deque(maxlen=max_queue_size))
prices = {'open':[], 'high':[], 'low':[], 'close':[]}

fig = go.Figure()

# Gives the last update from git commit
# @return a human readable string of when the last ~/z-algo git commit occurred
def last_updated():
    # Remote path
    #repo = git.Repo("~/z-algo").head.commit
    # Local path
    repo = git.Repo('~/Desktop/Zeppelin/z-algo').head.commit
    return time.strftime("%a, %d %b %Y %H:%M", time.gmtime(repo.committed_date))

#@return converted timestamp data to a human readable format
def time_conv(timestamp):
    return datetime.datetime.fromtimestamp(timestamp/ 1000).strftime('%Y-%m-%d %H:%M:%S.%f')[:-4]

# Takes data from on_message(ws, message) to return a graph existing graph and updates it on the dashboard
# @return the graph created from parsing the json response file
def data_processing(message):
    data = json.loads(message)

    # When receiving kline or miniTicker data:
    timestamps.append(time_conv(data['E']))
    prices['open'].append(data['o'])
    prices['high'].append(data['h'])
    prices['low'].append(data['l'])
    prices['close'].append(data['c'])

    # Other data types:
    '''
    #TODO

    '''
def make_graph():
    return fig

def register_callbacks(app):
    # Updates dashboard graph with websocket data
    @app.callback(Output('crypto-graph', 'figure'),
                [Input('interval', 'n_intervals')])
    def update_graph(_):
        # Update Figure object with new timestamp and price data
        fig.update_xaxes(range=[min(timestamps), max(timestamps)])
        fig.update_yaxes(range=[min(prices['low']), max(prices['high'])])
        fig.update_traces(
            x=timestamps,
            open=prices['open'],
            high=prices['high'],
            low=prices['low'],
            close=prices['close']
        )
        return fig