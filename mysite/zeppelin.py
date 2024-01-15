#!/usr/bin/env python
'''
@author Isaiah Terrell-Perica 
@date 05/26/2023

This file handles the display of the Zeppelin web-app.  
- The web-app requires:
    1) a dropdown selector with options (Trades, Portfolio, etc)
    2) financial indicators of interest
    3) a summary of the connected accounts' information
    4) option to choose strategies
- Zeppelin currently uses Binance for price data and account info
'''
import asyncio
import multiprocessing

from dash import dash, html, dcc

from backend import make_graph, last_updated, data_processing
from callback_updates import register_callbacks
from websocket_handling import start_websocket, close_websockets

app = dash.Dash(__name__)
server = app.server

# Retrieving components for Zeppelin
# Should make one main graph with subplots for each coin
coin_graphs = {
    #btc': make_graph("Bitcoin Price"),
    #'eth': make_graph("Etherium Price")

    # Function creates empty fig objects for each coin's graph
    0: make_graph("Bitcoin Price"),
    1: make_graph("Etherium Price")
}
time_interval=1000 # in milliseconds
shared_queue = multiprocessing.Queue(maxsize=1000)


# Dashboard layout
app.layout = html.Div(children=[
    html.H2(children="Zeppelin"),
    html.Div(children=f"Last commit: {last_updated()} UTC"),
    # List of all choices in [], then default selected choice
    dcc.Dropdown(['Coin Prices (Real Time)', 'Trades', 'Returns'], 'Coin Prices (Real Time)', id='dropdown'),
    dcc.Graph(id='btc-graph', figure=coin_graphs[0]),
    dcc.Graph(id='eth-graph', figure=coin_graphs[1]),
    dcc.Interval(id='interval', interval=time_interval, n_intervals=0),
    html.H3(children='Logs'),
    dcc.Textarea(id='logging', style={'width': '100%', 'height': '300px', 'backgroundColor': 'black',
                'color': 'white'}, persistence=True, readOnly=True)
])
register_callbacks(app, coin_graphs)

# Creates an event loop to run websocket url passed in
# @return the newly created event loop
def async_tasks(url, event):
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.create_task(start_websocket(url, event, shared_queue))
        loop.run_forever()
    finally:
        loop.call_soon_threadsafe(loop.create_task, end(loop))

# Starts websocket connections in separate processes
# @return array of multiprocessing processes created
def start_processes(event):
    # Array of urls to be connected to through websockets
    # New urls passed into websocket_handling.start_websocket(*)
    # Using raw trade information for highest fidelity
    urls = [
        'wss://testnet.binance.vision/ws/btcusdt@trade',
        'wss://testnet.binance.vision/ws/ethusdt@trade'
        #'wss://testnet.binance.vision/ws/btcusdt@kline_1m',
        #'wss://testnet.binance.vision/ws/ethusdt@kline_1m',
    ]
    processes = []
    # Create a process for each url with its own asyncio event loop
    for url in urls:
        process = multiprocessing.Process(target=async_tasks, daemon=True, args=(url, event))
        processes.append(process)
        process.start()
    return processes

# Close event loop
async def end(loop):
    await close_websockets()
    loop.run_until_complete(loop.shutdown_asyncgens())
    loop.stop()

if __name__ == '__main__':
    try:
        exit_event = asyncio.Event()
        # Create a process for each websocket and start it
        processes = start_processes(exit_event)
        # Create a process to handle data calculations
        data_process = multiprocessing.Process(target=data_processing, daemon=True, args=(shared_queue, exit_event))
        data_process.start()
        processes.append(data_process)
        # Run Zeppelin
        app.run_server(debug=True)
    finally:
        # Shutdown all processes, asyncio first
        # Set exit_event to True and end event loops
        exit_event.set()
        shared_queue.close()
        for process in processes:
            process.terminate()
            process.join()