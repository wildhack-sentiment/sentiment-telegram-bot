import boto3
import logging
from celery import shared_task
from django.conf import settings
from telegram import Bot

from app.helpers import AmplitudeLogger
from app.models import TelegramUser

# включаем логи
logger = logging.getLogger(__name__)

bot = Bot(settings.TELEGRAM_API_TOKEN)
s3 = boto3.client('s3')


@shared_task(name='bot.tasks.track_amplitude')
def track_amplitude(chat_id: int, event: str, event_properties=None, timestamp=None):
    if settings.AMPLITUDE_API_KEY is not None:
        amplitude = AmplitudeLogger(settings.AMPLITUDE_API_KEY)
        user = TelegramUser.objects.get(chat_id=chat_id)(chat_id=chat_id)
        amplitude.log(
            user_id=chat_id,
            event=event,
            user_properties={
                'Telegram chat ID': user.chat_id,
                'Name': user.full_name,
                'Telegram user name': user.user_name,
                'Daily catalog request limit': user.daily_catalog_requests_limit,
                'Subscribed to WB categories updates': user.subscribe_to_wb_categories_updates,
            },
            event_properties=event_properties,
            timestamp=timestamp,
        )
