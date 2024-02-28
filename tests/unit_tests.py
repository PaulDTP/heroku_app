import unittest
from unittest.mock import patch
import asyncio
import ccxt
import redis
import json
import decimal

from dash_app.logger import log_status

#from websocket_backend.exchanges import Client
#import websocket_backend.redis_handler as rh

# class AsyncTests(unittest.IsolatedAsyncioTestCase):
#     @classmethod
#     async def asyncSetUp(cls):
#         cls.instance = Client('binanceus')
#
#     @classmethod
#     async def asyncTearDown(cls):
#         await cls.instance.close_exchange()
#
#     async def test_create_exchange(self):
#         self.assertIsInstance(self.instance.exchange, ccxt.Exchange)
#
#     async def test_get_data(self):
#         await self.instance.exchange.load_markets()
#         data = await self.instance.exchange.fetchTicker('BTC/USDT')
#         self.assertIsInstance(data['high'], str)

class RedisTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Set up a mock Redis server for testing
        cls.redis_mock = patch("redis.Redis", autospec=True)
        cls.mock_instance = cls.redis_mock.start()

    @classmethod
    def tearDownClass(cls):
        # Stop mockRedis server after all tests
        cls.redis_mock.stop()

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_connection(self):
        pass

    # def redis_example(self):
    #     rh.to_redis("test")

class GeneralTests(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()