import time
import datetime

import dash
import pandas as pd
import numpy as np
import json
import git
from collections import defaultdict, deque
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import plotly.express as px

from logger import log_status, get_logs

max_queue_size = 1000
# X and Y axis data using deque for automatic resizing
timestamps = deque(maxlen=max_queue_size)
prices = defaultdict(lambda: deque(maxlen=max_queue_size))
# prices = {'open':[], 'high':[], 'low':[], 'close':[]}

fig = go.Figure()


# Gives the last update from git commit
# @return a human-readable string of when the last ~/z-algo git commit occurred
def last_updated():
    # Remote path
    # repo = git.Repo("~/z-algo").head.commit
    # Local path
    repo = git.Repo('~/Desktop/Zeppelin/z-algo').head.commit
    return time.strftime("%a, %d %b %Y %H:%M", time.gmtime(repo.committed_date))


# @return converted timestamp data to a human-readable format
def time_conv(timestamp):
    return datetime.datetime.fromtimestamp(timestamp / 1000).strftime('%Y-%m-%d %H:%M:%S.%f')[:-4]


# Takes data from on_message(ws, message) to process data for the dashboard graph
# @return the graph created from parsing the json response file
def data_processing(message):
    global timestamps, prices
    data = json.loads(message)

    # When receiving kline data:
    timestamps.append(time_conv(data['E']))
    prices['current'].append(float(data['p']))


def make_graph(title):
    fig.add_trace(go.Scatter(mode='lines'))
    fig.update_layout(
        title=title,
        showlegend=False,
        xaxis=dict(
            type="date",
            tickformat="%H:%M:%S"  # Customize the date format
        ),
        yaxis=dict(
            tickformat=".2f",
        )
    )
    return fig


# Receives callbacks to update dashboard graph
def register_callbacks(app):
    # Updates dashboard graph with websocket data
    @app.callback(
        [Output('crypto-graph', 'figure'),
         Output('logging', 'value')],
        [Input('interval', 'n_intervals')]
    )
    def update_graph(_):
        if not timestamps or not prices['current']:
            return dash.no_update
        x_axis = list(timestamps)
        current = list(prices['current'])

        # Extending y-axis for easier viewing
        price_min = min(current)
        price_max = max(current)
        extended_min = price_min - 0.25 * (price_max - price_min)
        extended_max = price_max + 0.25 * (price_max - price_min)

        # open_prices = list(prices['open'])
        # high_prices = list(prices['high'])
        # low_prices = list(prices['low'])
        # close_prices = list(prices['close'])

        # Update Figure object with new timestamp and price data
        fig.update_xaxes(range=[min(timestamps), max(timestamps)])
        fig.update_yaxes(range=[extended_min, extended_max])
        fig.update_traces(
            x=x_axis,
            y=current
        )
        # fig.update_traces(
        #     x=x_axis,
        #     open=open_prices,
        #     high=high_prices,
        #     low=low_prices,
        #     close=close_prices
        # )
        return fig, '\n'.join(get_logs())
