'''
@author Isaiah Terrell-Perica
@date 2024/01/24

This file creates an exchange object using CCXT and initializes its settings.
'''

import decimal
import os

import asyncio

import ccxt.pro as pro
import ccxt
import dotenv

async def create_exchange(exchange_name):
    '''
    Creates an exchange object using CCXT and initializes
    :param exchange_name: name of exchange to
    :return: exchange: async exchange object
    '''
    dotenv.load_dotenv()
    apiKey = os.getenv('TEST_API_KEY')
    apiSecret = os.getenv('TEST_API_SECRET')

    exch_class = getattr(pro, exchange_name)
    exchange = exch_class({'apiKey': apiKey, 'secret': apiSecret})
    exchange.set_sandbox_mode(True)
    exchange.number = decimal.Decimal
    await exchange.load_markets(reload=True)

    return exchange