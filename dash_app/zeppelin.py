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


app = dash.Dash(__name__, title="Zeppelin", update_title=None, add_log_handler=False)
server = app.server

# Retrieving components for Zeppelin
# Should make one main graph with subplots for each coin
# coin_graphs = {
#     0: make_graph("Bitcoin 1m Candles", 'candle'),
#     1: make_graph("Bitcoin Real-time Trades", 'line'),
#     # 1: make_graph("Etherium Price"),
# }
time_interval = 1000  # in milliseconds
tradingview = '''
 <!-- TradingView Widget BEGIN -->
<div class="tradingview-widget-container">
  <div class="tradingview-widget-container__widget"></div>
  <div class="tradingview-widget-copyright"><a href="https://www.tradingview.com/" rel="noopener nofollow" target="_blank"><span class="blue-text">Track all markets on TradingView</span></a></div>
  <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-advanced-chart.js" async>
  {
  "width": "100%",
  "height": "800",
  "symbol": "BINANCE:BTCUSDT",
  "interval": "1",
  "timezone": "Etc/UTC",
  "theme": "dark",
  "style": "1",
  "locale": "en",
  "enable_publishing": true,
  "withdateranges": true,
  "hide_side_toolbar": false,
  "allow_symbol_change": true,
  "watchlist": [
    "BINANCE:BTCUSDT",
    "NASDAQ:AAPL",
    "TVC:DJI",
    "AMEX:DIA",
    "AMEX:SPY"
  ],
  "details": true,
  "calendar": false,
  "support_host": "https://www.tradingview.com"
}
  </script>
</div>
<!-- TradingView Widget END -->
    '''

options = ['Chart', 'Real-time Trades']
# Dashboard layout
app.layout = html.Div(
    style={
        "display": "flex",
        'flex-direction': 'column'
    },
    children=[
    html.H2(children="Zeppelin"),
    #html.Div(children=f"Last commit: {last_updated()} UTC"),
    # List of all choices in [], then default selected choice
    #dcc.Dropdown([Prices', 'Real-time Trades'], 'Prices', id='dropdown'),
    dcc.Dropdown(options, options[0], id='dropdown'),
    html.Iframe(id='tradingview',srcDoc=tradingview, style={"height": "820px", "width": "calc(100% - 5vw)", "margin": '0 auto',
                                                            "border": "none", "justifyContent": "center", "align-items": "center"}
    ),
    #dcc.Graph(id='btc-candle', figure=coin_graphs[0]),
    #dcc.Graph(id='btc-trades', figure=coin_graphs[1]),
    #WebSocket(id='candle', url='wss://testnet.binance.vision/stream?streams=btcusdt@kline_1m'),
    #WebSocket(id='trades', url='wss://testnet.binance.vision/stream?streams=btcusdt@trade'),
    dcc.Interval(id='interval', interval=time_interval, n_intervals=0),
    html.H3(children='Logs'),
    dcc.Textarea(id='logging', style={'width': '100%', 'height': '300px', 'backgroundColor': 'black',
                                      'color': 'white'}, persistence=True, readOnly=True, persistence_type='local')
])

try:
    register_callbacks(app)#, coin_graphs)
    log_status("info", "Starting...")
    #app.run_server(debug=True)
except Exception as e:
    log_status("warning", f"Error: {e}")