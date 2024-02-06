from kombu import Exchange, Queue
import ssl

internal = 'redis://red-cmp9gj0l5elc73fo0k90:6379'
external = 'rediss://red-cmp9gj0l5elc73fo0k90:o4CD7EIFImOfGEGLr9KZAiG7KXI3ZTvB@oregon-redis.render.com:6379'
local = 'redis://localhost:6379/0'

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
    # task_serializer = 'json'
    # result_serializer = 'json'
    # accept_content = ['json']
    timezone = 'UTC'
    enable_utc = True
    broker_connection_retry_on_startup = True
    # task_queues = (
    #     Queue('graphing', Exchange('broadcast'), routing_key=''),
    #     Queue('graphing2', Exchange('broadcast'), routing_key='')
    # )