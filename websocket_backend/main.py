#!/usr/bin/env python
'''
@author: Isaiah Terrell-Perica
@data: 2024/01/25

This file runs the websocket connections and sends data to relevant processes.
Websocket -> Redis -> Celery -> PostgreSQL
'''
import asyncio
import json

from dash_app.logger import log_status
from websocket_backend.processes import start_backend, end_backend
from websocket_backend.exchanges import Client

async def main():
    client = Client('binanceus')
    await client.exchange.load_markets()

    try:
        # Connects to websockets through Client object
        await start_backend(client) # this line is blocking b/c of await
    except Exception as e:
        log_status('error', f'{e}')
    finally:
        await end_backend(client)

if __name__ == "__main__":
    asyncio.run(main())
