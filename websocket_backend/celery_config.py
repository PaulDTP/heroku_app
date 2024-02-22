from kombu import Exchange, Queue
import ssl

internal = 'redis://red-cmp9gj0l5elc73fo0k90:6379'
external = 'rediss://red-cmp9gj0l5elc73fo0k90:o4CD7EIFImOfGEGLr9KZAiG7KXI3ZTvB@oregon-redis.render.com:6379'
local = 'redis://localhost:6379/0'

db_url = ('postgres://zeppelin_user:taTZucupmhMbnEYXFZOHUkIXMFkSKEh9'
          '@dpg-cmlb7h6g1b2c73futgm0-a.oregon-postgres.render.com/zeppelin')

# celery -A celery_worker worker --loglevel=info
class CeleryConfig:
    broker_url = local
    result_backend = local
    # broker_transport_options = {'ssl_certs_reqs': ssl.CERT_NONE}
    # broker_use_ssl = {
    #     'ssl_cert_reqs': ssl.CERT_NONE
    # }
    # redis_backend_use_ssl = {
    #     'ssl_cert_reqs': ssl.CERT_NONE
    # }
    task_serializer = 'json'
    result_serializer = 'json'
    accept_content = ['json']
    timezone = 'UTC'
    enable_utc = True
    broker_connection_retry_on_startup = True
    worker_log_format = '[%(asctime)s: %(levelname)s/%(processName)s] %(message)s'
    worker_logfile = 'celery.log'
    # task_queues = (
    #     Queue('graphing', Exchange('broadcast'), routing_key=''),
    #     Queue('graphing2', Exchange('broadcast'), routing_key='')
    # )