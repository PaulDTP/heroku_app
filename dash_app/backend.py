"""
@author Isaiah Terrell-Perica
@date 05/31/2023

This file handles all calculations and data processing needed for coin graphs and technical indicators.

- May need to separate processing for data or conversions
- Should test time taken to run functions
"""
import json
import subprocess
from datetime import datetime
import plotly.graph_objs as go

import logging
from dash_app.logger import log_status


class MyFig(go.Figure):
    def __init__(self):
        super().__init__()
        self._open = []
        self._high = []
        self._low = []
        self._close = []


def last_updated():
    """
    Returns the last update from git commit
    :return: human-readable string of last ~/z-algo git commit
    """
    commit_date = subprocess.check_output(['git', 'log', '-1', '--format=%cd'])
    return commit_date.decode('utf-8').strip()


def make_graph(title, form):
    """
    Creates a blank graph ready for data
    :param title: title for created graph
    :param form: type of graph to make
    :return fig: blank Figure object
    """
    fig = MyFig()
    if form == 'candle':
        fig.add_trace(go.Candlestick(name='candle'))
    elif form == 'line':
        fig.add_trace(go.Scattergl(name='trade', mode='lines'))
    fig.update_layout(
        title=title,
        showlegend=False,
        xaxis=dict(
            type="date",
            tickformat="%H:%M:%S.%f"  # %Y-%m-%d"  # Customizing date format
        ),
        yaxis=dict(
            tickformat=".2f",  # Precision of y labels
        ),
        # maintains user state
        uirevision=True,
        xaxis_rangeslider_visible=False
    )
    return fig


def time_conv(timestamp):
    """
    Converts timestamp to a human-readable format
    :param timestamp: epoch time to convert
    :return: human-readable time
    """
    return datetime.fromtimestamp(timestamp / 1000).strftime('%Y-%m-%d %H:%M:%S.%f')


def data_processing(data):
    """
    Format:
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
    """
    print(data)
    sec_data = {}
    # symbol = data['s']  # Symbol (ex: BNBBTC)
    # event = data['e']  # Event type (kline, aggtrade, etc)
    timestamp = time_conv(data['E'])  # Event time ex: 1672515782136
    if data['e'] == 'trade':
        sec_data[timestamp] = float(data['p'])
    else:
        data = data['k']
        # timestamp = time_conv(data['t'])  # Candle start time ex: 1672515782000 -> interval start
        sec_data['time'] = timestamp
        sec_data['open'] = float(data['o'])
        sec_data['high'] = float(data['h'])
        sec_data['low'] = float(data['l'])
        sec_data['close'] = float(data['c'])
    return sec_data


def dict_processing(msg):
    """
    JSON loads format (must be string not dict):
    '{'e': 'trade',
     'E': 1708580838879,
     's': 'BTCUSDT',
     't': 1168941,
     'p': '51573.88000000',
     'q': '0.00010000',
     'b': 5630322,
     'a': 5630360,
     'T': 1708580838878,
     'm': True,
     'M': True}'
    :param msg: msg to parse
    :return sec_data: dict with key time and value price
    """
    sec_data = {}
    # if msg is in alt. format
    if 'stream' not in msg.keys():
        msg = json.loads(msg['data'])
    data = msg['data']

    # symbol = data['s']  # Symbol (ex: BNBBTC)
    # event = data['e']  # Event type (kline, aggtrade, etc)
    sec_data['time'] = time_conv(data['E'])  # Event time ex: 1672515782136
    if '@kline' in msg['stream']:
        # kline data
        data = data['k']
        # timestamp = time_conv(data['t'])  # Candle start time ex: 1672515782000 -> interval start
        # sec_data['time'] = timestamp
        sec_data['open'] = float(data['o'])
        sec_data['high'] = float(data['h'])
        sec_data['low'] = float(data['l'])
        sec_data['close'] = float(data['c'])
    elif '@trade' in msg['stream']:
        sec_data['value'] = float(data['p'])
    return sec_data