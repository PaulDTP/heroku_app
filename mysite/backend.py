'''
@author Isaiah Terrell-Perica
@date 05/31/2023

This file handles all calculations and data processing needed for coin graphs and technical indicators.

- May need to separate processing for data or conversions
- Should test time taken to run functions
'''
import datetime
import subprocess

import json
import plotly.graph_objs as go

from logger import log_status

max_queue_size = 1000

btc_timestamps = None
btc_prices = None
eth_timestamps = None
eth_prices = None


# Returns the last update from git commit
# @return a human-readable string of when the last ~/z-algo git commit occurred
def last_updated():
    commit_date = subprocess.check_output(['git', 'log', '-1', '--format=%cd'])
    return commit_date.decode('utf-8').strip()


# Creates a blank graph ready for data
# @return the initial graph 
def make_graph(title):
    fig = go.Figure()
    # fig.add_trace(go.Candlestick(name='main'))
    fig.add_trace(go.Scatter(name='main', mode='lines'))
    fig.update_layout(
        title=title,
        showlegend=False,
        xaxis=dict(
            type="date",
            tickformat="%H:%M:%S %Y-%m-%d"  # Customizing date format
        ),
        yaxis=dict(
            tickformat=".2f",  # Precision of y labels
        ),
        uirevision=True # maintains user state
    )
    return fig


# @return coin data requested from argument
def get_time_price(coin):
    if coin == 0 or coin == 'btc':
        return btc_timestamps, btc_prices
    if coin == 1 or coin == 'eth':
        return eth_timestamps, eth_prices


# @return a timestamp converted to a human-readable format
def time_conv(timestamp):
    return datetime.datetime.fromtimestamp(timestamp / 1000).strftime('%H:%M:%S.%f')[:-4]
    # .strftime('%Y-%m-%d %H:%M:%S.%f')[:-4]


def data_processing(shared_queue, exit_event, btimestamp, bprices, etimestamps, eprices):
    global btc_timestamps, btc_prices, eth_timestamps, eth_prices
    btc_timestamps = btimestamp
    btc_prices = bprices
    eth_timestamps = etimestamps
    eth_prices = eprices


    while not exit_event.is_set():
        print("processing")
        msg = shared_queue.get(block=True)
        data = json.loads(msg)
        symbol = data['s']  # Symbol (ex: BNBBTC)
        event = data['e']  # Event type (kline, aggtrade, etc)
        timestamp = time_conv(data['E'])  # Event time ex: 1672515782136
        # Bitcoin Websocket Handling     
        if symbol == 'BTCUSDT':
            # if timestamp not in btc_timestamps:
            btc_timestamps.append(timestamp)
            # Rolling window ticker stats (percent change, volume)
            if event == '24hrTicker':
                btc_prices['current'].append(float(data['c']))
            # Real-time trades
            elif event == 'trade':
                btc_prices['current'].append(float((data['p'])))
            elif event == 'kline':
                data = data['k']
                btc_prices['open'].append(float(data['o']))
                btc_prices['high'].append(float(data['h']))
                btc_prices['low'].append(float(data['l']))
                btc_prices['close'].append(float(data['c']))

        # Etherium Websocket Handling     
        elif symbol == 'ETHUSDT':
            eth_timestamps.append(timestamp)
            if event == '24hrTicker':
                eth_prices['current'].append(float(data['c']))
            elif event == 'trade':
                eth_prices['current'].append(float(data['p']))
            elif event == 'kline':
                data = data['k']
                eth_prices['open'].append(float(data['o']))
                eth_prices['high'].append(float(data['h']))
                eth_prices['low'].append(float(data['l']))
                eth_prices['close'].append(float(data['c']))

        # Other data types:
        '''
        #TODO
        '''


# Takes data from on_message(ws, message) to process data for the dashboard graph
# @return the graph created from parsing the json response file
'''def data_processing(message, url):
    global btc_timestamps, btc_timestamps, eth_prices, eth_timestamps
    data_lock.acquire(timeout=1)

    data = json.loads(message)
    symbol = data['s'] # Symbol (ex: BNBBTC)
    event = data['e'] # Event type (kline, aggtrade, etc)
    timestamp = time_conv(data['E']) # Event time ex: 1672515782136

    # Bitcoin Websocket Handling     
    if symbol == 'BTCUSDT':
        if timestamp not in btc_timestamps:
            btc_timestamps.append(timestamp)
        # Rolling window ticker stats (percent change, volume)
        if event == '24hrTicker':
            btc_prices['current'].append(float(data['c']))
        # Real-time trades
        elif event == 'trade':
            btc_prices['current'].append(float((data['p'])))
        elif event == 'kline':
            data = data['k']
            btc_prices['open'].append(float(data['o']))
            btc_prices['high'].append(float(data['h']))
            btc_prices['low'].append(float(data['l']))
            btc_prices['close'].append(float(data['c']))

    # Etherium Websocket Handling     
    elif symbol == 'ETHUSDT':
        eth_timestamps.append(timestamp)
        if event == '24hrTicker':
            eth_prices['current'].append(float(data['c']))
        elif event == 'trade':
            eth_prices['current'].append(float(data['p']))
        elif event == 'kline':
            data = data['k']
            eth_prices['open'].append(float(data['o']))
            eth_prices['high'].append(float(data['h']))
            eth_prices['low'].append(float(data['l']))
            eth_prices['close'].append(float(data['c']))
    data_lock.release()
'''
# Payload Types
'''
Trade Stream Payload
Update Speed: Real-time
{
  "e": "trade",     // Event type
  "E": 1672515782136,   // Event time
  "s": "BNBBTC",    // Symbol
  "t": 12345,       // Trade ID
  "p": "0.001",     // Price
  "q": "100",       // Quantity
  "b": 88,          // Buyer order ID
  "a": 50,          // Seller order ID
  "T": 1672515782136,   // Trade time
  "m": true,        // Is the buyer the market maker?
  "M": true         // Ignore
}

Candlesticks
Update Speed: 2000ms
{
  "e": "kline",     // Event type
  "E": 1672515782136,   // Event time
  "s": "BNBBTC",    // Symbol
  "k": {
    "t": 1672515780000, // Kline start time
    "T": 1672515839999, // Kline close time
    "s": "BNBBTC",  // Symbol
    "i": "1m",      // Interval
    "f": 100,       // First trade ID
    "L": 200,       // Last trade ID
    "o": "0.0010",  // Open price
    "c": "0.0020",  // Close price
    "h": "0.0025",  // High price
    "l": "0.0015",  // Low price
    "v": "1000",    // Base asset volume
    "n": 100,       // Number of trades
    "x": false,     // Is this kline closed?
    "q": "1.0000",  // Quote asset volume
    "V": "500",     // Taker buy base asset volume
    "Q": "0.500",   // Taker buy quote asset volume
    "B": "123456"   // Ignore
  }
}
24h Change 
Update Speed: 1000ms
{
  "e": "24hrTicker",  // Event type
  "E": 1672515782136,     // Event time
  "s": "BNBBTC",      // Symbol
  "p": "0.0015",      // Price change
  "P": "250.00",      // Price change percent
  "w": "0.0018",      // Weighted average price
  "x": "0.0009",      // First trade(F)-1 price (first trade before the 24hr rolling window)
  "c": "0.0025",      // Last price
  "Q": "10",          // Last quantity
  "b": "0.0024",      // Best bid price
  "B": "10",          // Best bid quantity
  "a": "0.0026",      // Best ask price
  "A": "100",         // Best ask quantity
  "o": "0.0010",      // Open price
  "h": "0.0025",      // High price
  "l": "0.0010",      // Low price
  "v": "10000",       // Total traded base asset volume
  "q": "18",          // Total traded quote asset volume
  "O": 0,             // Statistics open time
  "C": 1675216573749,      // Statistics close time
  "F": 0,             // First trade ID
  "L": 18150,         // Last trade Id
  "n": 18151          // Total number of trades
}

'''
