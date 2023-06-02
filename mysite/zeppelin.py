#!/usr/bin/env python
'''
Authored by Isaiah Terrell-Perica 
05/26/2023

This file handles the display of the Zeppelin web-app.  
- A Google Analytics tag is included but is not currently needed.
- The web-app requires:
    1) a dropdown selector with options
    2) indicators of interest clearly visualized
    3) a summary of the connected accounts' information
- Zeppelin currently uses Binance for price data and account info
'''
import asyncio

from dash import dash, html, dcc, Input, Output
import threading

import backend
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

# Creates Zeppelin using relevant Dash components
def create_zeppelin():
    # Retrieving components for Zeppelin
    crypto_graph = backend.make_graph()
    backend.register_callbacks(app)
    updated = backend.last_updated()
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
async def async_tasks():
    # Creating asynchronous tasks to be run in the event loop
    await start_websocket("binance")
    await close_websockets()

def start_thread():
    # Creating thread to run websockets in
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    t = threading.Thread(target=asyncio.run, args=(async_tasks(),), daemon=True)
    t.start()

# Run the Dash server
if __name__ == '__main__':
    create_zeppelin()
    start_thread()
    app.run_server(debug=True)