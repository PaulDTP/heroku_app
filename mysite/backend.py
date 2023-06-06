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
timestamps = deque(maxlen=max_queue_size)
prices = defaultdict(lambda: deque(maxlen=max_queue_size))
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
    return "Jun 6 1:33am EST"

#@return a timestamp converted to a human readable format
def time_conv(timestamp):
    return datetime.datetime.fromtimestamp(timestamp/ 1000).strftime('%Y-%m-%d %H:%M:%S.%f')[:-4]

# Takes data from on_message(ws, message) to process data for the dashboard graph
# @return the graph created from parsing the json response file
def data_processing(message):
    log_status('debug', 'Data received.')
    data = json.loads(message)

    # When receiving kline data:
    timestamp = time_conv(data['E'])
    timestamps.append(timestamp)
    data = data['k']
    prices['open'].append(float(data['o']))
    prices['high'].append(float(data['h']))
    prices['low'].append(float(data['l']))
    prices['close'].append(float(data['c']))

    # Other data types:
    '''
    #TODO
    '''

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

def update_data(fig):
    return fig

# Receives callbacks to update Zeppelin
# @return fig object holding Zeppelin
def register_callbacks(app, coin_graphs):
    # Updates dashboard graph with websocket data
    @app.callback(
        Output('bitcoin-graph', 'figure'),
        Output('etherium-graph', 'figure'),
        [Input('interval', 'n_intervals')]
    )
    def update_graph(_):
        bitcoin_fig = coin_graphs['bitcoin']
        etherium_fig = coin_graphs['etherium']

        # Only update the graph if data exists
        time_axis = list(timestamps)
        open_prices = list(prices['open'])
        if not time_axis or not open_prices:
            return dash.no_update

        # Casting data as list for congruency
        close_prices = list(prices['close'])
        low_prices = list(prices['low'])
        high_prices = list(prices['high'])

        # Extending y-axis for easier viewing
        price_min = min(low_prices)
        price_max = max(high_prices)
        extended_min = price_min - 0.5 * (price_max - price_min)
        extended_max = price_max + 0.5 * (price_max - price_min)

        # Update bitcoin_figure object with new timestamp and price data
        bitcoin_fig.update_xaxes(range=[min(time_axis), max(time_axis)])
        bitcoin_fig.update_yaxes(range=[extended_min, extended_max])
        bitcoin_fig.update_traces(
            x=time_axis,
            open=open_prices,
            high=high_prices,
            low=low_prices,
            close=close_prices
        )
        return bitcoin_fig, etherium_fig

    # Changes main page depending on dropdown selection
    # @return the selection made on the main page
    #@app.callback(Output('-graph'))
    def dropdown_changes(_):
        return fig