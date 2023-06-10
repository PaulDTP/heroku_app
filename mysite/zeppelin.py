#!/usr/bin/env python
'''
Authored by Isaiah Terrell-Perica 
05/26/2023

This file handles the display of the Zeppelin web-app.  
- A Google Analytics tag is included but is not currently needed.
- The web-app requires:
    1) a dropdown selector with options
    2) financialindicators of interest clearly visualized
    3) a summary of the connected accounts' information
- Zeppelin currently uses Binance for price data and account info
'''
import asyncio
import threading

from dash import dash, html, dcc

from backend import make_graph, last_updated
from callback_updates import register_callbacks
from websocket_streams import start_websocket, close_websockets

app = dash.Dash(__name__)
server = app.server

# Retrieving components for Zeppelin
coin_graphs = {
    #btc': make_graph("Bitcoin Price"),
    #'eth': make_graph("Etherium Price")
    0: make_graph("Bitcoin Price"),
    1: make_graph("Etherium Price")
}
register_callbacks(app, coin_graphs)
time_interval=1000 # in milliseconds

# Dashboard layout
app.layout = html.Div(children=[
    html.H2(children="Zeppelin"),
    html.Div(children=f"Last commit: {last_updated()} UTC"),
    dcc.Dropdown(['Coin Prices (Real Time)', 'Trades', 'Returns'], 'Coin Prices (Real Time)', id='dropdown'),
    dcc.Graph(id='btc-graph', figure=coin_graphs[0]),
    dcc.Graph(id='eth-graph', figure=coin_graphs[1]),
    dcc.Interval(id='interval', interval=time_interval),
    html.H3(children='Logs'),
    dcc.Textarea(id='logs', style={'width': '100%', 'height': '300px', 'backgroundColor': 'black',
                'color': 'white'}, persistence=True, readOnly=True)
])    

# Starts websocket connection and other asynchronous tasks with asyncio
def async_tasks(loop):
    # Array of urls to be connected to through websockets
    # - New urls must be added to start_websocket(*) also
    urls = [
        'wss://testnet.binance.vision/ws/btcusdt@kline_1m',
        'wss://testnet.binance.vision/ws/ethusdt@kline_1m'
    ]
    # Creating asynchronous tasks to be run in the event loop
    for x in urls:
        loop.create_task(start_websocket(x))
    loop.run_forever()

# Starts a new thread to run asyncio tasks
# @return the newly created event loop
def start_thread():
    # Creating thread to run websockets in
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    t = threading.Thread(target=async_tasks, args=(loop,), daemon=True)
    t.start()
    return loop

# Run the Dash server
if __name__ == '__main__':
    loop = start_thread()
    try:
        app.run_server(debug=True)
    finally:
        loop.call_soon_threadsafe(loop.create_task, close_websockets(loop))
        loop.stop()
