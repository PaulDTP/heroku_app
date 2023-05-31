import requests
import pandas as pd
import numpy as np

import websocket
import json
import git
import time


from binance.client import Client
import plotly.graph_objs as go
import plotly.express as px

# Binance
# API key: sN8B8IP18Sba4xi7X5aX2TaQtxMu8zxr5o2FkPxZvZBDXwwFT7Sl9VYzeILh4bCi
# secret key: 3BObFKszldGkDE9GjFe9YQpwPr0i0JJWVUGsU3EWR7KwDUCucDoVNl0GQwiOolkG

# Binance Spot Test Network: https://testnet.binance.vision/
# API Key: odwF9bVsSsxjZnckgbSu3NfUgGqqJ2sow4OelwjEttIBB08r3Z5umQL0A03lp2Gd
# Secret key: Q3bcPKvbvlVpzv5BQe3lj7EkWdRhevEp24Oi7TENce6xO0FiXUNQKDa47QTyyKcK

#testnet api
api_key='odwF9bVsSsxjZnckgbSu3NfUgGqqJ2sow4OelwjEttIBB08r3Z5umQL0A03lp2Gd'
api_secret='Q3bcPKvbvlVpzv5BQe3lj7EkWdRhevEp24Oi7TENce6xO0FiXUNQKDa47QTyyKcK'
# gets Binance user data from the Testnet using respective API key
client = Client(api_key, api_secret, testnet=True, tld='us');

# Maximum number of messages to receive before closing websocket
max_messages = 10
# Websocket base endpoint
wss = "wss://stream.binancefuture.com"
# Base endpoint
base = 'https://testnet.binancefuture.com'
# User data endpoint
user_data = '' # find in binance API
# x and y data
timestamps = []
prices = []

# Gives the last update from git commit
# @return a human readable string of when the last ~/z-algo git commit occurred
def last_updated():
    repo = git.Repo("/home/pauldtp/z-algo").head.commit
    return time.strftime("%a, %d %b %Y %H:%M", time.gmtime(repo.committed_date))

#@return converted timestamp data to a human readable format
def time_conv(timestamp):
    return datetime.datetime.fromtimestamp(timestamp/ 1000).strftime('%Y-%m-%d %H:%M:%S.%f')[:-4]

def on_open(ws):
    print("WebSocket connection opened")

# intended to update the dashboard graph after receiving data
def on_message(ws, message):
    data = json.loads(message)

    # when receiving kline or miniTicker data:
    prices = data['k']['c']
    timestamps.append(time_conv(data['E']))
    prices.append(y)

    # other data types:
    '''
    #TODO

    '''

    fig = go.Figure(data=[go.Candlestick(x=time_conv(data['E']),
                open=df['AAPL.Open'],
                high=df['AAPL.High'],
                low=df['AAPL.Low'],
                close=df['AAPL.Close'])])

    fig.add_trace(go.Scatter(x=timestamps, y=y_data, mode='lines', name='Bitcoin Price'))
    fig.update_layout(title='Bitcoin Price', xaxis_title='Time', yaxis_title='Price (USD)')
    fig.show()

    # Terminate the WebSocket connection after reaching the maximum number of messages
    if len(timestamps) >= max_messages:
        ws.close()

def on_error(ws, error):
    print("WebSocket error:", error)

def on_close(ws):
    print("WebSocket connection closed")

# Takes data from on_message(ws, message) to return a graph existing graph and updates it on the dashboard
# @return the graph created from parsing the json response file
def make_graph():
    ws_url = 'wss://testnet.binance.vision/ws/btcusdt@kline_1m'
    # Make the API call
    ws = websocket.WebSocketApp(
        url=ws_url,
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )
    data = response.json()
    # need to access data somewhere here

    # Store the data in a Pandas dataframe
    df = pd.DataFrame(data, index=[0])
    # Plot the data
    fig = px.line(df, x=timestamp, y="price")
    return fig

x_data = []
y_data = []



