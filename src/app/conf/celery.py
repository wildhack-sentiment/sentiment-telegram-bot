from app.conf.environ import env

# Celery conf
# https://docs.celeryproject.org/en/stable/userguide/configuration.html

CELERY = {
    'broker_url': env('REDIS_URL'),
    'broker_transport_options': {
        'max_retries': 3,
        'interval_start': 0,
        'interval_step': 0.2,
        'interval_max': 0.5,
        'visibility_timeout': 3600 * 48,
    },
    'result_backend': 'django-db',

    'redis_max_connections': env('CELERY_REDIS_MAX_CONNECTIONS', cast=int, default=None),
    'task_always_eager': env('CELERY_ALWAYS_EAGER', cast=bool, default=True),
    'task_reject_on_worker_lost': env('CELERY_TASK_REJECT_ON_WORKER_LOST', cast=bool, default=True),
    'task_serializer': 'pickle',  # we transfer binary data like photos or voice messages,
    'accept_content': ['pickle'],
    'timezone': env('TIME_ZONE', cast=str, default='UTC'),
    'enable_utc': True,
}
