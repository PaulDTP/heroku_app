#!/usr/bin/env python
'''
@author Isaiah Terrell-Perica 
@date 05/26/2023

This file handles the display of the Zeppelin web-app.  
- The web-app requires:
    1) a dropdown selector with options (Trades, Portfolio, etc.)
    2) financial indicators of interest
    3) a summary of the connected accounts' information
    4) option to choose strategies
- Zeppelin currently uses Binance for price data and account info
'''
from dash import dash, html, dcc

from backend import make_graph, last_updated
from callback_updates import register_callbacks
from processes import start_backend, end_backend
from websocket_streams import open_websocket

app = dash.Dash(__name__)
server = app.server

# Retrieving components for Zeppelin
# Should make one main graph with subplots for each coin
coin_graphs = {
    0: make_graph("Bitcoin Price"),
}
time_interval = 1000  # in milliseconds

# Dashboard layout
app.layout = html.Div(children=[
    html.H2(children="Zeppelin"),
    html.Div(children=f"Last commit: {last_updated()} UTC"),
    # List of all choices in [], then default selected choice
    dcc.Dropdown(['Coin Prices (Real Time)', 'Trades', 'Returns'], 'Coin Prices (Real Time)', id='dropdown'),
    dcc.Graph(id='btc-graph', figure=coin_graphs[0]),
    dcc.Interval(id='interval', interval=time_interval, n_intervals=0),
    html.H3(children='Logs'),
    dcc.Textarea(id='logging', style={'width': '100%', 'height': '300px', 'backgroundColor': 'black',
                                      'color': 'white'}, persistence=True, readOnly=True)
])
register_callbacks(app, coin_graphs)

if __name__ == '__main__':
    try:
        start_backend()
        app.run_server(debug=False, threaded = False)
    finally:
        end_backend()

# postgres://zeppelin_user:taTZucupmhMbnEYXFZOHUkIXMFkSKEh9@dpg-cmlb7h6g1b2c73futgm0-a/zeppelin

