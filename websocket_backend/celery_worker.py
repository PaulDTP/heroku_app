'''
@author Isaiah Terrell-Perica
@date 1/25/24

This file handles Celery task processing.
'''

from celery import Celery
from celery_config import CeleryConfig
from kombu import Exchange, Queue

celery = Celery('zep')
celery.config_from_object(CeleryConfig)