'''
Authored by Isaiah Terrell-Perica 
06/06/2023
This file handles callbacks for all Dash components in Zeppelin.
'''

from dash import dash, Input, Output

from backend import get_time_price
from logger import get_logs

# Receives callbacks to update Zeppelin
# @return fig object holding Zeppelin
def register_callbacks(app, coin_graphs):
    # Updates dashboard graph with websocket data
    @app.callback(
        Output('bitcoin-graph', 'figure'),
        Output('etherium-graph', 'figure'),
        Output('logs', 'value'),
        [Input('interval', 'n_intervals')]
    )
    def updates(_):
        timestamps, prices = get_time_price()
        bitcoin_fig = coin_graphs['bitcoin']
        etherium_fig = coin_graphs['etherium']

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
        extended_min = price_min - 0.5 * (price_max - price_min)
        extended_max = price_max + 0.5 * (price_max - price_min)

        # Update bitcoin_figure object with new timestamp and price data
        bitcoin_fig.update_xaxes(range=[min(time_axis), max(time_axis)])
        bitcoin_fig.update_yaxes(range=[extended_min, extended_max])
        bitcoin_fig.update_traces(
            x=time_axis,
            open=open_prices,
            high=high_prices,
            low=low_prices,
            close=close_prices
        )

        logs = get_logs()
        return bitcoin_fig, etherium_fig, '\n'.join(logs)

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