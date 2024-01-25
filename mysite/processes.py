'''
@author Isaiah Terrell-Perica 
@date 01/15/2024

This file handles multiprocessing for Zeppelin functionality.  
- Processes:
    1) Each websocket created
    2) Analysis of incoming data
'''
import threading
import multiprocessing
import asyncio

from websocket_streams import open_websocket, close_websocket
from backend import data_processing

exit_event = asyncio.Event()
loop = asyncio.get_event_loop()
processes = []


# Starts websocket connections in separate processes
# @return array of multiprocessing processes created
def start_websockets(shared_queue):
    # Array of urls to be connected to through websockets
    # New urls passed into websocket_handling.start_websocket(*)
    # Using raw trade information for highest fidelity
    urls = [
        'wss://testnet.binance.vision/ws/btcusdt@trade',
    ]
    # loop = asyncio.get_event_loop()
    asyncio.set_event_loop(loop)
    for url in urls:
        loop.create_task(open_websocket(url, exit_event, shared_queue))
    loop.run_forever()


# Close event loop
def end():
    loop.call_soon_threadsafe(loop.create_task, close_websocket())
    loop.stop()


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


# Starts processes for websockets and data
def start_backend():
    manager = multiprocessing.Manager()
    shared_queue = shared_data(manager, 'queue')

    # Thread for websocket connection
    ws = threading.Thread(target=start_websockets, args=(shared_queue, ))
    ws.start()

    # Process for CPU data tasks
    process = multiprocessing.Process(
        target=data_processing,
        daemon=True,
        args=(shared_queue, exit_event, shared_data(manager, 'list'), shared_data(manager, 'dict'), shared_data(manager,
            'list'), shared_data(manager, 'dict'))
    )
    processes.append(process)
    process.start()


# Sets exit event and closes multiprocessing processes
def end_backend():
    print("Killing processes")
    end()
    exit_event.set()
    for process in processes:
        process.join()
        process.close()
