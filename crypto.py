import requests
import time
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