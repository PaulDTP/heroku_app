'''
Authored by Isaiah Terrell-Perica
05/31/2023
This file handles all websocket connections and data, calling inherited functions for processing and visualization.
'''

import os
from dotenv import load_dotenv
import websocket
import json

from backend import data_processing

#testnet api
load_dotenv()
api_key=os.getenv('TEST_API_KEY')
api_secret=os.getenv('TEST_API_SECRET')
# Counts number of messages received
num_messages = 0

def on_open(ws):
    print("WebSocket connection opened")

#  Updates the dashboard graph after receiving data
def on_message(ws, message):
    global num_messages
    data_processing(message)
    num_messages += 1

    # Terminate the WebSocket connection after reaching the maximum number of messages
    if num_messages >= 1000:
        if ws.sock and ws.sock.connected:
            ws.close()
        else:
            print("WebSocket connection is already closed.")

def on_error(ws, error):
    print("WebSocket error:", error)

def on_close(ws, close_status_code, close_msg):
    if ws.sock and ws.sock.connected:
        print(close_status_code)
        print(close_msg)
        print("WebSocket connection closed.")
    else:
        print("WebSocket connection is already closed.")

def start_websocket():
    ws_url = 'wss://testnet.binance.vision/ws/btcusdt@trade'
    # Make the API call
    ws = websocket.WebSocketApp(
        url=ws_url,
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )
    ws.run_forever()