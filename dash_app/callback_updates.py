'''
@author Isaiah Terrell-Perica 
@date 06/06/2023

This file handles graph updates - callbacks for all Dash components in Zeppelin.

From docs: 'callbacks should never modify variables outside of their scope - do not modify global variables'
'''
from dash import dash, Input, Output
from datetime import datetime
import time

from backend import data_processing
from logger import get_logs, log_status
from zep_redis import from_redis

NUM_COINS = 2

# Would prefer to not have global
all_times = []
all_prices = []

# Updates a fig graph depending on the coin type
def update(fig):
    global all_times, all_prices
    data = from_redis()
    sec_data = data_processing(data)

    # Only update graphs if data exists
    if not sec_data:
        return dash.no_update

    format = '%Y-%m-%d %H:%M:%S'
    time = list(map(lambda x: datetime.strptime(x, format), sec_data.keys()))
    price = list(map(float, sec_data.values()))

    all_times += time
    all_prices += price

    #log_status("info",f"Updating graph with {len(prices)} prices")

    # Extending y-axis for easier viewing
    price_min = min(all_prices)
    price_max = max(all_prices)
    extended_min = price_min - 0.25 * (price_max - price_min)
    extended_max = price_max + 0.25 * (price_max - price_min)

    fig.update_xaxes(range=[min(all_times), max(all_times)])
    fig.update_yaxes(range=[price_min, price_max])

    # I want to have 2 graphs, one of the candlestick (main)
    # and one with a line connecting the current price (aux) of a given moment.
    '''fig.update_traces(
        x=time_axis,
        open=open_prices,
        high=high_prices,
        low=low_prices,
        close=close_prices,
        selector=dict(name="aux") # will be main
    )'''
    fig.update_traces(
        x=all_times,
        y=all_prices,
        selector=dict(name="main")
    )
    return fig


# Receives callbacks to update Zeppelin
def register_callbacks(app, coin_graphs):
    # Updates dashboard graph with websocket data
    # @return the output for all graphs on the main page for Zeppelin
    @app.callback(
        [Output('btc-graph', 'figure'),
         Output('logging', 'value')],
        [Input('interval', 'n_intervals')]
    )
    def updates(_):
        return update(coin_graphs[0]), '\n'.join(get_logs())

    # Changes Zeppelin's main page depending on dropdown selection
    # @return the selection made on main page
    # @app.callback(Output('*-graph'))
    # def dropdown_changes(_):
    #    return figs[coin]

    '''@app.callback(
        Output('logs', 'value'),
        Input('interval', 'n_intervals')
    )'''

    # def download(_):
    #     logs = get_logs()
    #     return '\n'.join(logs)
