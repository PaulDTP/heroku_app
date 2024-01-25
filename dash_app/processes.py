'''
@author Isaiah Terrell-Perica 
@date 01/15/2024

This file handles multiprocessing for Zeppelin functionality.  
- Processes:
    1) Each websocket created
    2) Analysis of incoming data
'''
import time
import threading


import asyncio

from websocket_streams import open_websocket, close_websocket
from backend import data_processing
import exchanges
from logger import log_status

exit_event = asyncio.Event()
exchange = None
processes = []

def shared_data(manager, data):
    maxlen = 1000
    if data == 'dict':
        return manager.dict({'current': []})
    if data == 'queue':
        return manager.Queue(maxsize=maxlen)
    if data == 'list':
        return manager.list()
    else:
        return "Error"

async def open_websocket(exchange, symbol):
    time_processed = []
    while not exit_event.is_set():
        start_time = time.time()
        try:
            async with exchange.watch_trade(symbol) as ticker:
                log_status('info', f"WebSocket connection for {symbol} opened")
                async for trade in ticker:
                    print(trade['asks'], trade['bids'])
                    time_processed.append(time.time() - start_time)
                    log_status('debug', f'{time_processed}')
        except Exception as e:
            log_status('error', f"Error with websocket: {e}")

async def start_websockets(exchange):
    '''
    Starts websocket connections
    :param shared_queue:

    '''
    symbols = ['BTC/USDT']  # , 'ETH/USDT', 'ETH/BTC']

    loop = asyncio.get_event_loop()
    asyncio.set_event_loop(loop)

    await loop.gather(*[open_websocket(exchange, symbol) for symbol in symbols])


# Starts processes for websockets and data
def start_backend():
    '''
    Starts backend processes for websockets and exchange connections
    :return:
    '''
    global exchange
    exchange = exchanges.create_exchange('binance.us')
    ws = threading.Thread(target=start_websockets, args=(exchange))
    ws.start()

# Sets exit event and closes multiprocessing processes
def end_backend():
    print("Ending")
    exit_event.set()
    asyncio.run_coroutine_threadsafe(exchange.close())