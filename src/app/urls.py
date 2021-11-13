from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from app import views as BotViews

urlpatterns = []

# Telegram bot
urlpatterns += [
    path('', BotViews.index, name='index'),
    path(f'{settings.TELEGRAM_API_TOKEN}', csrf_exempt(BotViews.TelegramBotWebhookView.as_view()), name='telegram_webhook'),
]

# Django admin
urlpatterns += [
    path('admin/', admin.site.urls),
]
