from django.conf import settings
from django.core.management.base import BaseCommand
from telegram import Bot

from app.bot import reset_webhook


class Command(BaseCommand):
    help = 'Reset Telegram webhook'  # noqa: VNE003

    def handle(self, *args, **options):
        bot = Bot(settings.TELEGRAM_API_TOKEN)

        reset_webhook(bot, settings.TELEGRAM_WEBHOOKS_DOMAIN, settings.TELEGRAM_API_TOKEN)

        self.stdout.write(self.style.SUCCESS('All done'))
