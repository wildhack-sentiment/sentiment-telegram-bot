from django.contrib import admin

from app.models import Command, TelegramUser


@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ('chat_id', 'user_name', 'full_name', 'created_at')


@admin.register(Command)
class LogCommandItemAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'command', 'message', 'status', 'created_at')
