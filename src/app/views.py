import json
import logging
from django.conf import settings
from django.http import JsonResponse
from django.views import View
from telegram import Bot, Update

from app.bot import start_bot

logger = logging.getLogger(__name__)


def index(request):
    return JsonResponse({'status': 'lucky_you'})


class TelegramBotWebhookView(View):
    def post(self, request, *args, **kwargs):
        bot = Bot(settings.TELEGRAM_API_TOKEN)
        bot_dispatcher = start_bot(bot)

        bot_dispatcher.process_update(Update.de_json(json.loads(request.body), bot))

        return JsonResponse({'status': 'ok'}, status=200)
