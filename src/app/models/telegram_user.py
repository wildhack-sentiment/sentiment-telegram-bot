from django.db import models


class TelegramUser(models.Model):
    """Модель пользователя в телеграме."""

    #: ID чата, по которому может быть идентифицирован пользователь
    chat_id = models.IntegerField(primary_key=True)

    #: Имя пользователя
    user_name = models.CharField(blank=True, max_length=255)

    #: Фамилия пользователя
    full_name = models.CharField(blank=True, max_length=255)

    #: Заблокирован ли пользовтаель
    catalog_requests_blocked = models.BooleanField(default=False)

    #: Дата создания объекта
    created_at = models.DateTimeField(auto_now_add=True)

    #: Дата последнего обновления объекта
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'app_telegram_user'
        verbose_name = 'bot user'
        verbose_name_plural = 'bot users'

        indexes = [
            models.Index(fields=['user_name']),
            models.Index(fields=['full_name']),
            models.Index(fields=['created_at']),
            models.Index(fields=['updated_at']),
        ]

    def __str__(self):
        return self.chat_id

    def can_send_more_requests(self) -> bool:
        """Может ли пользователь отправлять еще запросы на анализ"""
        return True
