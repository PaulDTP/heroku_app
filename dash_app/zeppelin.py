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
from dash import dash, html, dcc, Output, Input
from dash_extensions import WebSocket

from dash_app.backend import make_graph, last_updated
from dash_app.callback_updates import register_callbacks
from dash_app.zep_redis import create_rclient, close_redis
from dash_app.callback_updates import update
from dash_app.logger import get_logs, log_status


app = dash.Dash(__name__, title="Zeppelin")
server = app.server

# Retrieving components for Zeppelin
# Should make one main graph with subplots for each coin
coin_graphs = {
    0: make_graph("Bitcoin Price"),
    # 1: make_graph("Etherium Price"),
}
time_interval = 1000  # in milliseconds

# Dashboard layout
app.layout = html.Div(children=[
    html.H2(children="Zeppelin"),
    #html.Div(children=f"Last commit: {last_updated()} UTC"),
    # List of all choices in [], then default selected choice
    #dcc.Dropdown(['Coin Prices (Real Time)', 'Trades', 'Returns'], 'Coin Prices (Real Time)', id='dropdown'),
    dcc.Dropdown(['Coin Prices (Real-time Trades)'], 'Coin Prices (Real-time Trades)', id='dropdown'),
    dcc.Graph(id='btc-graph', figure=coin_graphs[0]),
    WebSocket(id='ws', url='wss://testnet.binance.vision/ws/btcusdt@trade'),
    dcc.Interval(id='interval', interval=time_interval, n_intervals=0),
    html.H3(children='Logs'),
    dcc.Textarea(id='logging', style={'width': '100%', 'height': '300px', 'backgroundColor': 'black',
                                      'color': 'white'}, persistence=True, readOnly=True, persistence_type='local')
])
# update_graph = """function(msg) {
#     if(!msg){return {};}  // no data, just return
#     const data = JSON.parse(msg.data);  // read the data
#     return {data: [{y: data, type: "scatter"}]}};  // plot the data
# """
# app.clientside_callback(update_graph, Output("btc-graph", "figure"), Input("ws", "message"))

try:
    #create_rclient()
    register_callbacks(app, coin_graphs)
    #app.run_server(debug=False, host='0.0.0.0', port=8050)
finally:
    log_status("info", "Starting...")
    #close_redis()