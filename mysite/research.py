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

price_data = np.array([])

# Binance Initialization
from binance.client import Client

api_key='sN8B8IP18Sba4xi7X5aX2TaQtxMu8zxr5o2FkPxZvZBDXwwFT7Sl9VYzeILh4bCi'
api_secret='3BObFKszldGkDE9GjFe9YQpwPr0i0JJWVUGsU3EWR7KwDUCucDoVNl0GQwiOolkG'

client = Client(api_key, api_secret, testnet=True, tld='us')

for i in range(21600):
    resp = requests.get('https://api.binance.us/api/v3/ticker/price?symbol=BTCUSD')
    price_data = np.append(price_data, resp.json()['price'])
    price_data.tofile('prices.csv', sep=',')
    time.sleep(4)


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