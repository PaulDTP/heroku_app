#!/home/pauldtp/.virtualenvs/zeppelin/bin/python

# Binance
# API key: sN8B8IP18Sba4xi7X5aX2TaQtxMu8zxr5o2FkPxZvZBDXwwFT7Sl9VYzeILh4bCi
# secret key: 3BObFKszldGkDE9GjFe9YQpwPr0i0JJWVUGsU3EWR7KwDUCucDoVNl0GQwiOolkG 

# Binance Spot Test Network: https://testnet.binance.vision/
# API Key: iLqNC7LgXSOH6CDbgVAuyMIYhTwXI2FoeCDJzjLKMBbjBx1hg8i5RbTDs8WJEC3G
# Secret key: o8Jyhbtt9pCPzDeIQcntwSjSKdQ67jemQIIh1n4XN72YMrEi3gOzfRuQZpSxec4W

import requests
import plotly.express as px
import pandas as pd
import numpy as np

from binance.client import Client
import plotly.graph_objs as go
import websocket
import json

api_key='sN8B8IP18Sba4xi7X5aX2TaQtxMu8zxr5o2FkPxZvZBDXwwFT7Sl9VYzeILh4bCi'
api_secret='3BObFKszldGkDE9GjFe9YQpwPr0i0JJWVUGsU3EWR7KwDUCucDoVNl0GQwiOolkG'

client = Client(api_key, api_secret, testnet=True, tld='us')

url = "wss://stream.binancefuture.com"

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

