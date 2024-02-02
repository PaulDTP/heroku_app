'''
@author Isaiah Terrell-Perica
@date 1/25/24

This file handles Redis processing.
'''

import redis
from dash_app.logger import log_status

redis_client = None

def create_client():
    global redis_client
    external = 'rediss://red-cmp9gj0l5elc73fo0k90:o4CD7EIFImOfGEGLr9KZAiG7KXI3ZTvB@oregon-redis.render.com:6379'
    internal = 'localhost'
    redis_client = redis.Redis(host=external, port=6379)

def to_redis(data):
    if redis_client is None:
        log_status("error", "Redis client not initialized.")
    #redis_client.rpush('trades_queue', data)
    else:
        redis_client.publish('test', data)

def first_elem():
    if redis_client is None:
        log_status("error", "Redis client not initialized.")
    #redis_client.rpush('trades_queue', data)
    else:
        return redis_client.lpop('trades_queue')

def close_redis():
    if redis_client is None:
        log_status("error", "Redis client not initialized.")
    else:
        redis_client.close()