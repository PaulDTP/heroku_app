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
# X and Y axis data using deque for automatic resizing
timestamps = deque(maxlen=max_queue_size)
prices = defaultdict(lambda: deque(maxlen=max_queue_size))
#prices = {'open':[], 'high':[], 'low':[], 'close':[]}

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

# Takes data from on_message(ws, message) to process data for the dashboard graph
# @return the graph created from parsing the json response file
def data_processing(message):
    data = json.loads(message)

    # When receiving kline data:
    timestamps.append(time_conv(data['E']))
    data = data['k']
    prices['open'].append(data['o'])
    prices['high'].append(data['h'])
    prices['low'].append(data['l'])
    prices['close'].append(data['c'])

    # Other data types:
    '''
    #TODO
    '''

def make_graph():
    fig.add_trace(go.Candlestick())
    fig.update_layout(
            showlegend=False,
            xaxis=dict(
            type="date",
            tickformat="%H:%M:%S %Y-%m-%d"  # Customize the date format
            ),
            yaxis=dict(
                tickformat=".2f",
            )
        )
    return fig

# Receives callbacks to update dashboard graph
def register_callbacks(app):
    # Updates dashboard graph with websocket data
    @app.callback(Output('crypto-graph', 'figure'),
                [Input('interval', 'n_intervals')])
    def update_graph(_):

        x_axis = list(timestamps)
        open_prices = list(prices['open'])
        high_prices = list(prices['high'])
        low_prices = list(prices['low'])
        close_prices = list(prices['close'])

        # Update Figure object with new timestamp and price data
        fig.update_xaxes(range=[min(timestamps), max(timestamps)])
        fig.update_yaxes(range=[min(low_prices), max(high_prices)])
        fig.update_traces(
            x=x_axis,
            open=open_prices,
            high=high_prices,
            low=low_prices,
            close=close_prices
        )
        return fig