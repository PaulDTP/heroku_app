'''
Authored by Isaiah Terrell-Perica 
06/06/2023
This file handles callbacks for all Dash components in Zeppelin.
'''
import threading

from dash import dash, Input, Output

from backend import get_time_price
from logger import get_logs

NUM_COINS = 2
data_lock = threading.Lock()

# Receives callbacks to update Zeppelin
# @return figs[coin] object holding Zeppelin
def register_callbacks(app, coin_graphs):
    # Updates dashboard graph with websocket data
    @app.callback(
        Output('btc-graph', 'figure'),
        Output('eth-graph', 'figure'),
        Output('logging', 'value'),
        [Input('interval', 'n_intervals')]
    )
    def updates(_):
        # Graph data for all coins
        # - should put all this in for loops later for parallelism
        # - Should make coin objects
        figs = []
        data_lock.acquire()
        #figs[coin] = [update_graph(coin_graphs[coin]) for coin in range(NUM_COINS)]
        try:
            for coin in range(NUM_COINS):
                timestamps, prices = get_time_price(coin)
                figs.append(coin_graphs[coin])
                
                # Only update graphs if data exists
                if not timestamps or not prices:
                    return dash.no_update

                current_price = list(prices['current'])
                time_axis = list(timestamps)

                '''
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
                figs[coin].update_xaxes(range=[min(time_axis), max(time_axis)])
                figs[coin].update_yaxes(range=[min(current_price), max(current_price)])
                figs[coin].update_traces(
                    x=time_axis,
                    y=list(prices['current']),
                    selector=dict(name="aux")
                )
                logs = get_logs()
        finally:
            data_lock.release()
            return figs[0], figs[1], '\n'.join(logs)

    # Changes main page depending on dropdown selection
    # @return the selection made on the main page
    #@app.callback(Output('-graph'))
    def dropdown_changes(_):
        return figs[coin]

    '''@app.callback(
        Output('logs', 'value'),
        Input('interval', 'n_intervals')
    )'''
    def download(_):
        logs = get_logs()
        return '\n'.join(logs)