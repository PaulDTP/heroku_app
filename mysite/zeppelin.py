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

from dash import dash, html, dcc, Input, Output
import threading

from backend import make_graph, last_updated, register_callbacks
from websocket_streams import start_websocket, close_websockets

app = dash.Dash(__name__)

# Google Analytics tag
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        <!-- Google tag (gtag.js) -->
        <script async src="https://www.googletagmanager.com/gtag/js?id=G-WMWKTVG0WM"></script>
        <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());

        gtag('config', 'G-WMWKTVG0WM');
        </script>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# Retrieving components for Zeppelin
crypto_graph = make_graph()
register_callbacks(app)
updated = last_updated()
time_interval=1000 # in milliseconds

# Dashboard layout
app.layout = html.Div(children=[
    html.H2(children="Zeppelin"),
    html.Div(children=f"Last commit: {updated} UTC"),
    dcc.Dropdown(['Coin Prices (Real Time)', 'Trades', 'Returns'], 'Coin Prices (Real Time)', id='dropdown'),
    dcc.Graph(id='crypto-graph', figure=crypto_graph),
    dcc.Interval(id='interval', interval=time_interval)
    #, generate_table(data)
])    

# Starts websocket connection and other asynchronous tasks with asyncio
def async_tasks(loop):
    # Array of exchanges to be connected to through websockets
    # - New exchanges must be added to start_websocket(*) also
    exchanges = ['binance']
    # Creating asynchronous tasks to be run in the event loop
    for x in exchanges:
        loop.create_task(start_websocket(x))
    loop.run_forever()
    #await asyncio.gather(*tasks)

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