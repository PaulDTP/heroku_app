'''
@author Isaiah Terrell-Perica 
@date 06/06/2023

This file handles graph updates - callbacks for all Dash components in Zeppelin.

From docs: 'callbacks should never modify variables outside of their scope - do not modify global variables'
'''
from dash import dash, Input, Output

from backend import get_time_price
from logger import get_logs, log_status

NUM_COINS = 2


# Updates a fig graph depending on the coin type
def update(fig, coin):
    timestamps, prices = get_time_price(coin)
    # Only update graphs if data exists
    if not timestamps or (not prices['current'] and not prices['open']):
        return dash.no_update
    print("updating...")
    current_price = list(prices['current'])
    time_axis = list(timestamps)

    # Extending y-axis for easier viewing
    price_min = min(current_price)
    price_max = max(current_price)
    extended_min = price_min - 0.25 * (price_max - price_min)
    extended_max = price_max + 0.25 * (price_max - price_min)

    fig.update_xaxes(range=[min(time_axis), max(time_axis)])
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
        x=time_axis,
        y=current_price,
        selector=dict(name="main")  # will be aux
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
        return update(coin_graphs[0], 'btc'), '\n'.join(get_logs())

    # Changes Zeppelin's main page depending on dropdown selection
    # @return the selection made on main page
    # @app.callback(Output('*-graph'))
    # def dropdown_changes(_):
    #    return figs[coin]

    '''@app.callback(
        Output('logs', 'value'),
        Input('interval', 'n_intervals')
    )'''

    def download(_):
        logs = get_logs()
        return '\n'.join(logs)
