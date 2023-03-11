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

# api eee8e2d1bfc46b546f74a0152e841ead60322a3eebe9197dc8aed462fb35c13c
# secret 6644db47ed44d9da102b3c9134d52324769a8079c8c89dd1cee365d4f88d0889


api_key='sN8B8IP18Sba4xi7X5aX2TaQtxMu8zxr5o2FkPxZvZBDXwwFT7Sl9VYzeILh4bCi'
api_secret='3BObFKszldGkDE9GjFe9YQpwPr0i0JJWVUGsU3EWR7KwDUCucDoVNl0GQwiOolkG'

client = Client(api_key, api_secret, testnet=True, tld='us')

# Websocket base endpoint
wss = "wss://stream.binancefuture.com"
# Base endpoint
base = 'https://testnet.binancefuture.com'
# User date endpoint


def get_updated():
    # Last update from git commit
    repo = git.Repo("/home/pauldtp/z-algo").head.commit
    return time.strftime("%a, %d %b %Y %H:%M", time.gmtime(repo.committed_date))

def make_graph():
    # Make the API call
    url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
    response = requests.get(url)
    data = response.json() 

    # Store the data in a Pandas dataframe
    df = pd.DataFrame(data, index=[0])

    # Plot the data
    fig = px.line(df, x=df.index, y="price")
    return fig

x_data = []
y_data = []

def on_message(ws, message):
    data = json.loads(message)
    y = data['k']['c']
    x_data.append(data['E'])
    y_data.append(y)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_data, y=y_data, mode='lines', name='Bitcoin Price'))
    fig.update_layout(title='Bitcoin Price', xaxis_title='Time', yaxis_title='Price (USD)')
    fig.show()

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://stream.binance.com:9443/ws/btcusdt@kline_1m",
                                on_message=on_message)
    ws.run_forever()

