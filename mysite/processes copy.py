'''
@author Isaiah Terrell-Perica 
@date 01/15/2024

This file handles multiprocessing for Zeppelin functionality.  
- Processes:
    1) Each websocket created
    2) Analysis of incoming data
'''
import asyncio
import multiprocessing

from websocket_handling import open_websocket, close_websocket
from backend import data_processing

shared_queue = multiprocessing.Queue(maxsize=1000)
exit_event = asyncio.Event()
loop = asyncio.get_event_loop()
processes = []

# Starts websocket connections in separate processes
# @return array of multiprocessing processes created
def start_websocket(event):
    # Array of urls to be connected to through websockets
    # New urls passed into websocket_handling.start_websocket(*)
    # Using raw trade information for highest fidelity
    urls = [
        'wss://testnet.binance.vision/ws/btcusdt@trade',
    ]
    #loop = asyncio.get_event_loop()
    asyncio.set_event_loop(loop)

    # Create a process for each url with its own asyncio event loop
    for url in urls:
        loop.create_task(open_websocket(url, exit_event, shared_queue))
    loop.run_forever()

# Close event loop
def end():
    loop.run_until_complete(close_websocket())
    loop.stop()
    loop.run_until_complete(loop.shutdown_asyncgens())
    loop.close()

# Starts processes for websockets and data
def start_backend():
    # Start websocket processes
    websocket_process = multiprocessing.Process(target=start_websocket, daemon=True, args=(exit_event,))
    with websocket_process as ws:
        ws.start()
    # Create a process to handle data calculations
    data_process = multiprocessing.Process(target=data_processing, daemon=True, args=(shared_queue, exit_event))
    with data_process as dp:
        dp.start()

    # Add processes to open process list
    #processes.append(data_process)
    #processes.append(websocket_process)

# Sets exit event and closes multiprocessing processes
def end_backend():
    print("killing processes")
    end()
    exit_event.set()
    shared_queue.close()