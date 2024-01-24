from mysite.logger import log_status
import os
from dotenv import load_dotenv
from binance.spot import Spot as Client
from binance.websocket.spot.websocket_stream import SpotWebsocketStreamClient

load_dotenv()
api_key = os.getenv("TEST_API_KEY2")
api_secret = os.getenv("TEST_API_SECRET2")

def message_handler(_, message):
    log_status('info', message)
def message_handler(message):
    log_status('info', message)

def create_client():
    client = Client(api_key, api_secret, base_url='https://testnet.binance.vision')
    response = client.new_listen_key()
    log_status('info', f"Received listen key: {response}")
    return client, response
if __name__ == '__main__':
    try:
        client, response = create_client()
        ws_client = SpotWebsocketStreamClient(stream_url="wss://testnet.binance.vision", on_message=message_handler)
        ws_client.user_data(listen_key=response["listenKey"])
    except:
        print("whoops")
        pass
    finally:
        ws_client.stop()
