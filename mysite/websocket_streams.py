'''
Authored by Isaiah Terrell-Perica
05/31/2023
This file handles all websocket connections and data, calling inherited functions for processing.
'''
import asyncio
import time

import websockets
import json
#from binance.client import Client

from backend import data_processing
from logger import log_status

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
##client = Client(api_key, api_secret, testnet=True, tld='us');

# Websocket base endpoint
# wss = "wss://stream.binancefuture.com"
# Base endpoint
# base = 'https://testnet.binancefuture.com'
# User data endpoint
user_data = '' # find in binance API
open_websockets = []

# Close all open websockets
async def close_websockets(loop):
    log_status('info', "Closing all websockets...")
    for ws in open_websockets.copy():
        try:
            open_websockets.remove(ws)
            await ws.close()
        except Exception as e:
            log_status('error', f"Error closing websocket: {e}")
        else:
            open_websockets.remove(ws)
    log_status('info', "Done")

# Starts websocket connections and calls appropriate processing function(s)
async def start_websocket(type):
    global open_websockets
    print('starting websocket')
    try:
        if type == 'binance':
            async with websockets.connect('wss://testnet.binance.vision/ws/btcusdt@kline_1m') as ws:
                log_status('info', "WebSocket connection opened")
                open_websockets.append(ws)
                while True:
                    #start_time = time.time()
                    data = await ws.recv()
                    #elapsed_time = time.time() - start_time
                    #print(f"Received data in {elapsed_time} seconds: {data}")
                    data_processing(data)
    except websockets.exceptions.ConnectionClosedError:
        log_status('info', "WebSocket connection closed")        