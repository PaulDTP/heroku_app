"""
@author Isaiah Terrell-Perica
@date 1/15/2024

This file handles websocket connections for Zeppelin functionality.
- Processes:
    1) Each websocket created for symbol pairs
    2) Incoming data sent to required function for processing

Incoming data from websocket is in format:
[{'info': {'e': 'trade', 'E': 1708540575663, 's': 'BTCUSDT', 't': 1133073, 'p': '51062.17000000',
'q': '0.00063000', 'b': 5459029, 'a': 5459025, 'T': 1708540575662, 'm': False, 'M': True},
'timestamp': 1708540575662, 'datetime': '2024-02-21T18:36:15.662Z', 'symbol': 'BTC/USDT',
'id': '1133073', 'order': None, 'type': None, 'side': 'buy', 'takerOrMaker': None, 'price': '51062.17000000',
'amount': '0.00063000', 'cost': '32.1691671', 'fee': None, 'fees': []}]
"""
import time
import asyncio

#from ws_backend import data_processing
from dash_app.logger import log_status
from websocket_backend.celery_worker import process_data
from dash_app.zep_redis import create_rclient, close_redis, to_redis

exit_event = asyncio.Event()

client = None

async def open_websocket(exchange, symbol):
    time_processed = []
    if 'watchTrades' in exchange.has:  # line exists for understanding, you must check methods exist with CCXT
        log_status('info', f"WebSocket connection for {symbol} opened")
        while not exit_event.is_set():
            start_time = time.time()
            try:
                # returns list of dicts containing trade info
                data = await exchange.watchTrades(symbol)
                to_redis(data)
            except Exception as e:
                log_status('error', f"Error in websocket: {e}")
            finally:
                time_processed.append(time.time() - start_time)
    else:
        log_status('warning', 'Exchange doesn\'t have method.')


# Starts processes for websockets and data
async def start_backend(client):
    """
    Starts backend processes for websockets and exchange connections
    :param client: Exchange instance
    """
    symbols = ['BTC/USDT']  # , 'ETH/USDT', 'ETH/BTC']
    create_rclient()
    await asyncio.gather(*[open_websocket(client.exchange, symbol) for symbol in symbols])


async def end_backend(client):
    """
    Sets exit event and closes exchange connections
    :param client: Instance wrapping CCXT exchange objet
    """
    log_status('info', 'Ending backend processes.')
    exit_event.set()
    #close_redis()
    await client.close_exchange()