from django.db import models

from app.models.telegram_user import TelegramUser


class Command(models.Model):
    """Модель истории запросов от пользователя к боту."""

    #: Ссылка на контакт Телеграма
    user = models.ForeignKey(TelegramUser, on_delete=models.DO_NOTHING, related_name='commands', db_constraint=False)

    #: Текст команды
    command = models.TextField(blank=True)

    #: Текст сообщения
    message = models.TextField(blank=True)

    #: Статус исполнения запроса
    status = models.CharField(blank=True, max_length=255)

    #: Дата приема запроса
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'app_commands'
        verbose_name = 'command'
        verbose_name_plural = 'commands'

        indexes = [
            models.Index(fields=['command']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return self.message

    def set_status(self, status):
        self.status = status
        self.save()
        return self
