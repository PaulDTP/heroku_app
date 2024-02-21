'''
@author Isaiah Terrell-Perica
@date 1/25/24

This file handles Celery task processing.
'''

from celery import Celery
from websocket_backend.celery_config import CeleryConfig
from kombu import Exchange, Queue
import redis
import json

from logger import log_status

celery = Celery('zep')
celery.config_from_object(CeleryConfig)

# celery -A celery_worker worker --loglevel=info

@celery.task
def process_data(data):
    if data:
        data = json.loads(data)
        for trade in data:
            #construct_frame()
            pass