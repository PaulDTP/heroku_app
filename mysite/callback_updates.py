'''
@author Isaiah Terrell-Perica 
@date 06/06/2023

This file handles graph updates - callbacks for all Dash components in Zeppelin.

From docs: 'callbacks should never modify variables outside of their scope - do not modify global variables'
'''
import threading

from dash import dash, Input, Output

from backend import get_time_price
from logger import get_logs, log_status

NUM_COINS = 2
data_lock = threading.Lock()

# Updates a fig graph depending on the coin type
def update(fig, coin):
    data_lock.acquire(timeout=1)
    timestamps, prices = get_time_price(coin)

    # Only update graphs if data exists
    if not timestamps or not prices['current'] or not prices['open']:
        raise PreventUpdate

    current_price = list(prices['current'])
    time_axis = list(timestamps)

    # Casting data as list for congruency
    open_prices = list(prices['open'])
    close_prices = list(prices['close'])
    low_prices = list(prices['low'])
    high_prices = list(prices['high'])

    # Extending y-axis for easier viewing
    price_min = min(low_prices)
    price_max = max(high_prices)
    extended_min = price_min - 0.25 * (price_max - price_min)
    extended_max = price_max + 0.25 * (price_max - price_min)

    fig.update_xaxes(range=[min(time_axis), max(time_axis)])
    fig.update_yaxes(range=[price_min, price_max])

    # I want to have 2 graphs, one of the candlestick (main), and one with a line connecting the current price (aux) of a given moment.
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
        selector=dict(name="main") # will be aux
    )
    data_lock.release()
    return fig

# Receives callbacks to update Zeppelin
def register_callbacks(app, coin_graphs):
    # Updates dashboard graph with websocket data
    # @return the output for all graphs on the main page for Zeppelin
    @app.callback(
        [Output('btc-graph', 'figure'),
        Output('eth-graph', 'figure'),
        Output('logging', 'value')],
        [Input('interval', 'n_intervals')]
    )
    def updates(_):
        # Graph data for all coins
        # - should put all this in for loops later for parallelism
        # - Should make coin objects
        #figs[coin] = [update_graph(coin_graphs[coin]) for coin in range(NUM_COINS)]]
        '''
        for coin in range(NUM_COINS):
            # Casting data as list for congruency
            open_prices = list(prices['open'])
            close_prices = list(prices['close'])
            low_prices = list(prices['low'])
            high_prices = list(prices['high'])

            # Extending y-axis for easier viewing
            price_min = min(low_prices)
            price_max = max(high_prices)

            # Analyze this
            extended_min = price_min - 0.5 * (price_max - price_min)
            extended_max = price_max + 0.5 * (price_max - price_min)

            # Update btc_figure object with new timestamp and price data
            figs[coin].update_xaxes(range=[min(time_axis), max(time_axis)])
            figs[coin].update_yaxes(range=[extended_min, extended_max])
            figs[coin].update_traces(
                x=time_axis,
                open=open_prices,
                high=high_prices,
                low=low_prices,
                close=close_prices,
                selector=dict(name="main")
            )
            '''
        return update(coin_graphs[0], 'btc'), update(coin_graphs[1], 'eth'), '\n'.join(get_logs())

    # Changes Zeppelin's main page depending on dropdown selection
    # @return the selection made on main page
    #@app.callback(Output('*-graph'))
    def dropdown_changes(_):
        return figs[coin]

    '''@app.callback(
        Output('logs', 'value'),
        Input('interval', 'n_intervals')
    )'''
    def download(_):
        logs = get_logs()
        return '\n'.join(logs)