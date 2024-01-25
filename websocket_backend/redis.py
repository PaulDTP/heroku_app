'''
@author Isaiah Terrell-Perica
@date 1/25/24

This file handles Redis processing
'''

import redis

external_url =  'rediss://red-cmp9gj0l5elc73fo0k90:o4CD7EIFImOfGEGLr9KZAiG7KXI3ZTvB@oregon-redis.render.com:6379'
redis_client = redis.Redis(host=external_url, port=6379)



def to_redis(data):
    redis_client.publish('zeppelin', data)