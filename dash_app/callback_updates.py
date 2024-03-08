"""
@author Isaiah Terrell-Perica 
@date 06/06/2023

This file handles graph updates - callbacks for all Dash components in Zeppelin.

From docs: 'callbacks should never modify variables outside their scope - do not modify global variables'
"""
from datetime import datetime

from dash import dash, Input, Output

from dash_app.backend import data_processing, dict_processing
from dash_app.logger import get_logs, log_status

# Would prefer to not have global
trade_times = []
candle_times = []
trade_prices = []
candle_prices = []
fmt = '%Y-%m-%d %H:%M:%S.%f'


def update(fig, msg):
    """
    Updates Figure object from argument with data in msg
    :param fig: Figure to be updated
    :param msg: Websocket data to parse
    """
    global trade_times, candle_times, trade_prices, candle_prices
    # data = from_redis()

    data = msg

    # Only update graph if data exists
    if not data:
        return dash.no_update
    # Determine call based on msg format
    if isinstance(msg, dict):
        sec_data = dict_processing(msg)
    else:
        sec_data = data_processing(data)
    # Kline Data
    if len(sec_data) == 5:
        return update_candle(fig, sec_data)
    # Trade Data
    else:
        return update_trades(fig, sec_data)


def update_candle(fig, sec_data):
    global candle_times, candle_prices
    fig._open.append(sec_data['open'])
    fig._high.append(sec_data['high'])
    fig._low.append(sec_data['low'])
    fig._close.append(sec_data['close'])
    candle_times.append(datetime.strptime(sec_data['time'], fmt))
    fig.update_traces(
        x=candle_times,
        open=fig._open,
        high=fig._high,
        low=fig._low,
        close=fig._close,
        selector=dict(name="candle")
    )
    return fig


def update_trades(fig, sec_data):
    global trade_times, trade_prices
    trade_times.append(datetime.strptime(sec_data['time'], fmt))
    trade_prices.append(sec_data['value'])
    fig.update_traces(
        x=trade_times,
        y=trade_prices,
        selector=dict(name="trade")
    )
    return fig


def register_callbacks(app, coin_graphs):
    """
    Updates dashboard based on type of input
    :param app: Dash app
    :param coin_graphs: dict holding Figure objects for securities
    :return fig, str: Figure object and log lines to output
    """

    @app.callback(
        Output('logging', 'value'),
        Input('interval', 'n_intervals'),
        prevent_initial_call=True
    )
    def update_log(_):
        return '\n'.join(get_logs())

    # === Candles ===
    @app.callback(
        Output('btc-candles', 'figure'),
        Input("ws-candles", 'message'),
        prevent_initial_call=True
    )
    def update_c(msg):
        log_status("info", "Candle data received")
        data = dict_processing(msg)
        if data is None:
            return dash.no_update
        return update_candle(coin_graphs[0], data)

    # === Trades ===
    @app.callback(
        Output('btc-trades', 'figure'),
        Input("ws-trades", 'message'),
        prevent_initial_call=True
    )
    def update_t(msg):
        log_status("info", "Trade data received")
        data = dict_processing(msg)
        if data is None:
            return dash.no_update
        return update_trades(coin_graphs[1], data)
