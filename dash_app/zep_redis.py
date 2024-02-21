'''
@author Isaiah Terrell-Perica
@date 1/25/24

This file handles Redis processing for Zeppelin.
'''

import redis
import json
from decimal import Decimal
from dash_app.logger import log_status

redis_client = None

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return str(o)
        return super(DecimalEncoder, self).default(o)

def create_rclient():
    global redis_client
    external = 'rediss://red-cmp9gj0l5elc73fo0k90:o4CD7EIFImOfGEGLr9KZAiG7KXI3ZTvB@oregon-redis.render.com:6379'
    internal = 'localhost'
    redis_client = redis.Redis(host=internal, port=6379)
    log_status("info", "Redis client created")

def to_redis(data):
    if redis_client is None:
        log_status("error", "Redis client not initialized.")
    else:
        log_status("info", "Websocket data received")
        redis_client.rpush('queue', json.dumps(data, cls=DecimalEncoder))

def from_redis():
    if redis_client is None:
        log_status("error", "Redis client not initialized.")
    else:
        return json.loads(redis_client.lpop('queue'))


def close_redis():
    if redis_client is None:
        log_status("error", "Redis client not initialized.")
    else:
        redis_client.close()