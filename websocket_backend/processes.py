'''
@author Isaiah Terrell-Perica 
@date 1/15/2024

This file handles multiprocessing for Zeppelin functionality.  
- Processes:
    1) Each websocket created
    2) Analysis of incoming data
'''
import time
import asyncio

from websocket_streams import open_websocket, close_websocket
from backend import data_processing
from dash_app.logger import log_status
from exchanges import Client
from redis_handler import create_client, to_redis, close_redis

exit_event = asyncio.Event()

async def open_websocket(exchange, symbol):
    time_processed = []
    if 'watchTrades' in exchange.has: # line exists for understanding, you must check methods exist with CCXT
        log_status('info', f"WebSocket connection for {symbol} opened")
        while not exit_event.is_set():
            start_time = time.time()
            try:
                data = await exchange.watchTrades(symbol)
                to_redis(data)
                process.delay()
            except Exception as e:
                log_status('error', f"Error in websocket: {e}")
            finally:
                time_processed.append(time.time() - start_time)
    else:
        log_status('warning', 'Exchange doesn\'t have method.')


# Starts processes for websockets and data
async def start_backend(client):
    '''
    Starts backend processes for websockets and exchange connections
    '''
    symbols = ['BTC/USDT']  # , 'ETH/USDT', 'ETH/BTC']
    create_client()
    await asyncio.gather(*[open_websocket(client.exchange, symbol) for symbol in symbols])


async def end_backend(client):
    '''
    Sets exit event and closes exchange connections
    :param client: Instance wrapping CCXT exchange objet
    '''
    log_status('info', 'Ending backend processes.')
    exit_event.set()
    await client.close_exchange()
    close_redis()