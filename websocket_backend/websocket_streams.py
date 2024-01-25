'''
Authored by Isaiah Terrell-Perica
05/31/2023
This file handles all websocket connections and the resulting data, calling inherited functions for processing.
'''
import time

import websockets

from dash_app.logger import log_status

# Starts websocket connections and calls appropriate processing function(s)
async def open_websocket(url, event, shared_queue, exchange):
    global open_websockets, time_processed
    try:
        async with websockets.connect(url) as ws:
            log_status('info', f"WebSocket connection for {url} opened")
            open_websockets.append(ws)
            while not event.is_set():
                start_time = time.time()
                data = await ws.recv()
                # storing data in shared data struct
                shared_queue.put(data) # SEND data to database here
                time_processed.append(time.time() - start_time)
                log_status('debug', f'{time_processed}')
    except Exception as e:
        log_status('error', f"Error with websocket: {e}")


# Close all open websockets
async def close_websocket():
    global open_websockets
    for ws in open_websockets.copy():
        try:
            open_websockets.remove(ws)
            await ws.close()
        except Exception as e:
            log_status('error', f"Error closing websocket: {e}")