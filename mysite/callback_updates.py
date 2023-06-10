'''
Authored by Isaiah Terrell-Perica 
06/06/2023
This file handles callbacks for all Dash components in Zeppelin.
'''
from dash import dash, Input, Output

from backend import get_time_price
from logger import get_logs

NUM_COINS = 2

# Receives callbacks to update Zeppelin
# @return fig object holding Zeppelin
def register_callbacks(app, coin_graphs):
    # Updates dashboard graph with websocket data
    figs = []
    @app.callback(
        Output('btc-graph', 'figure'),
        Output('eth-graph', 'figure'),
        Output('logs', 'value'),
        [Input('interval', 'n_intervals')]
    )
    def updates(_):
        # Graph data for all coins
        # - should put all this in for loops later for parallelism
        # - Should make coin objects
        for coin in range(0, NUM_COINS):
            timestamps, prices = get_time_price(coin)
            fig = coin_graphs[coin]
            # Only update the graph if data exists
            time_axis = list(timestamps)
            open_prices = list(prices['open'])
            if not time_axis or not open_prices:
                return dash.no_update

            # Casting data as list for congruency
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
            fig.update_xaxes(range=[min(time_axis), max(time_axis)])
            fig.update_yaxes(range=[extended_min, extended_max])
            fig.update_traces(
                x=time_axis,
                open=open_prices,
                high=high_prices,
                low=low_prices,
                close=close_prices
            )
            logs = get_logs()
        return fig, '\n'.join(logs)

    # Changes main page depending on dropdown selection
    # @return the selection made on the main page
    #@app.callback(Output('-graph'))
    def dropdown_changes(_):
        return fig

    '''@app.callback(
        Output('logs', 'value'),
        Input('interval', 'n_intervals')
    )'''
    def download(_):
        logs = get_logs()
        return '\n'.join(logs)