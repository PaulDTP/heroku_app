'''
Authored by Isaiah Terrell-Perica
05/31/2023
This file handles all websocket connections and data, calling inherited functions for processing and visualization.
'''
import asyncio
import time

import websockets
import json
from binance.client import Client

from backend import data_processing

# Binance
# API key: sN8B8IP18Sba4xi7X5aX2TaQtxMu8zxr5o2FkPxZvZBDXwwFT7Sl9VYzeILh4bCi
# secret key: 3BObFKszldGkDE9GjFe9YQpwPr0i0JJWVUGsU3EWR7KwDUCucDoVNl0GQwiOolkG

# Binance Spot Test Network: https://testnet.binance.vision/
# API Key: odwF9bVsSsxjZnckgbSu3NfUgGqqJ2sow4OelwjEttIBB08r3Z5umQL0A03lp2Gd
# Secret key: Q3bcPKvbvlVpzv5BQe3lj7EkWdRhevEp24Oi7TENce6xO0FiXUNQKDa47QTyyKcK

# Testnet API
api_key='odwF9bVsSsxjZnckgbSu3NfUgGqqJ2sow4OelwjEttIBB08r3Z5umQL0A03lp2Gd'
api_secret='Q3bcPKvbvlVpzv5BQe3lj7EkWdRhevEp24Oi7TENce6xO0FiXUNQKDa47QTyyKcK'
# Gets Binance user data from the Testnet using respective API key
client = Client(api_key, api_secret, testnet=True, tld='us');

# Websocket base endpoint
# wss = "wss://stream.binancefuture.com"
# Base endpoint
# base = 'https://testnet.binancefuture.com'
# User data endpoint
user_data = '' # find in binance API
open_websockets = []

# Close all open websockets
#TODO change print statements to log statements
async def close_websockets():
    print("Closing all websockets...")
    for ws in open_websockets.copy():
        await ws.close()
        open_websockets.remove(ws)
    print("Done")

# Define the WebSocket connection logic
async def start_websocket(type):
    global open_websockets
    try:
        if type == 'binance':
            async with websockets.connect('wss://testnet.binance.vision/ws/btcusdt@kline_1m') as ws:
                print("WebSocket connection opened")
                open_websockets.append(ws)
                while True:
                    #start_time = time.time()
                    data = await ws.recv()
                    #elapsed_time = time.time() - start_time
                    #print(f"Received data in {elapsed_time} seconds: {data}")
                    data_processing(data)
    except websockets.exceptions.ConnectionClosedError:
        print("WebSocket connection closed")        

'''# Start the WebSocket connection in a separate task
async def hmm_websocket(type):
    await connect_websocket(type)
'''

