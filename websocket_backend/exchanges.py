'''
@author Isaiah Terrell-Perica
@date 2024/01/24

This file creates an exchange object using CCXT/Pro and initializes its settings.
'''

import decimal
import os

import asyncio
import ccxt.pro as pro
import ccxt
import dotenv

from dash_app.logger import log_status

class Client:
    '''
    Client class wraps a CCXT object to provide custom methods and attributes.

    Attributes:
        name (str): The name of the exchange.
        exchange (object): The CCXT object.
    Methods:
        close_exchange(self): Closes the exchange object.

    '''
    dotenv.load_dotenv()
    apiKey = os.getenv('TEST_API_KEY')
    apiSecret = os.getenv('TEST_API_SECRET')
    open_exchanges = []

    def __init__(self, name):
        self.name = name
        exch_class = getattr(pro, name)
        self.exchange = exch_class({'enableRateLimit': True,
                           'apiKey': Client.apiKey, 'secret': Client.apiSecret})
        self.exchange.set_sandbox_mode(True)
        self.exchange.number = str #decimal.Decimal
        Client.open_exchanges.append(self.name)

    async def close_exchange(self):
        '''
        Closes the exchange for cleanup
        :param self: exchange to be closed
        '''
        await self.exchange.close()
        if self.name in Client.open_exchanges:
            Client.open_exchanges.remove(self.name)
            log_status('info', f'Exchange closed: {self.name}')