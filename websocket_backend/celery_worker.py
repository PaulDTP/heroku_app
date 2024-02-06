'''
@author Isaiah Terrell-Perica
@date 1/25/24

This file handles Celery task processing.
'''

from celery import Celery
from celery_config import CeleryConfig
from kombu import Exchange, Queue
import redis
import json

from logger import log_status

celery = Celery('zep')
celery.config_from_object(CeleryConfig)

@celery.task
def process(data):
    if data:
        data = json.loads(data)
        log_status('info', f'{data}')
        log_status('info', f'{type(data)}')
