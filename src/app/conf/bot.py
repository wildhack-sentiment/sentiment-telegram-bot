from app.conf.environ import env

TELEGRAM_API_TOKEN = env('TELEGRAM_API_TOKEN', cast=str, default='')
TELEGRAM_WEBHOOKS_DOMAIN = env('TELEGRAM_WEBHOOKS_DOMAIN', cast=str, default='')
