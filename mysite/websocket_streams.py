'''
Authored by Isaiah Terrell-Perica
05/31/2023
This file handles all websocket connections and the resulting data, calling inherited functions for processing.
'''
import time

import websockets
#from binance.client import Client

from logger import log_status

# Binance - real account
# API key: sN8B8IP18Sba4xi7X5aX2TaQtxMu8zxr5o2FkPxZvZBDXwwFT7Sl9VYzeILh4bCi
# secret key: 3BObFKszldGkDE9GjFe9YQpwPr0i0JJWVUGsU3EWR7KwDUCucDoVNl0GQwiOolkG

# Binance Spot Test Network: https://testnet.binance.vision/
api_key='odwF9bVsSsxjZnckgbSu3NfUgGqqJ2sow4OelwjEttIBB08r3Z5umQL0A03lp2Gd'
api_secret='Q3bcPKvbvlVpzv5BQe3lj7EkWdRhevEp24Oi7TENce6xO0FiXUNQKDa47QTyyKcK'

# Gets Binance user data from the Testnet using respective API key
# client = Client(api_key, api_secret, testnet=True, tld='us');

# Websocket base endpoint
# wss = "wss://stream.binancefuture.com"

# Base endpoint
# base = 'wss://testnet.binance.vision'
# User data endpoint
user_data = '' # find in binance API

# Will list all websockets that are opened
open_websockets = []
time_processed = []


# Starts websocket connections and calls appropriate processing function(s)
async def open_websocket(url, event, shared_queue):
    global open_websockets, time_processed
    try:
        async with websockets.connect(url) as ws:
            log_status('info', f"WebSocket connection for {url} opened")
            open_websockets.append(ws)
            while not event.is_set():
                start_time = time.time()
                data = await ws.recv()
                # storing data in shared data struct
                shared_queue.put(data) # SEND data to database here
                time_processed.append(time.time() - start_time)
                log_status('debug', f'{time_processed}')
    except Exception as e:
        log_status('error', f"Error with websocket: {e}")


# Close all open websockets
async def close_websocket():
    global open_websockets
    for ws in open_websockets.copy():
        try:
            open_websockets.remove(ws)
            await ws.close()
        except Exception as e:
            log_status('error', f"Error closing websocket: {e}")