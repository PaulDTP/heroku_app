import unittest
import asyncio
import ccxt

from websocket_backend.exchanges import Client

class Tests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.instance = Client('binanceus')

    async def asyncTearDown(self):
        await self.instance.close_exchange()

    async def test_create_exchange(self):
        self.assertIsInstance(self.instance.exchange, ccxt.Exchange)

if __name__ == '__main__':
    unittest.main()