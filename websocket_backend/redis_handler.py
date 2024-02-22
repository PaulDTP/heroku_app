'''
@author Isaiah Terrell-Perica
@date 1/25/24

This file handles Redis processing.
'''

import redis
import json

from dash_app.logger import log_status
from websocket_backend.celery_worker import process_data

redis_client = None


def create_client():
    global redis_client
    external = 'rediss://red-cmp9gj0l5elc73fo0k90:o4CD7EIFImOfGEGLr9KZAiG7KXI3ZTvB@oregon-redis.render.com:6379'
    internal = 'localhost'
    redis_client = redis.Redis(host=internal, port=6379)

def to_redis(data):
    if redis_client is None:
        log_status("error", "Redis client not initialized.")
    else:
        redis_client.rpush('queue', json.dumps(data))
        process_data.delay(redis_client.lpop("queue"))


def close_redis():
    if redis_client is None:
        log_status("error", "Redis client not initialized.")
    else:
        redis_client.close()