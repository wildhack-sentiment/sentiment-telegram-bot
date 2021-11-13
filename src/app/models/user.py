from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager as _UserManager
from django.db import models


class UserManager(_UserManager):
    pass


class User(AbstractUser):
    """Модель пользователя."""

    objects = UserManager()

    #: Дата последнего визита
    last_visit = models.DateTimeField(auto_now_add=True, null=True)

    #: Дата добавления пользователя
    created_at = models.DateTimeField(auto_now_add=True)

    #: Дата последнего обновления пользователя
    updated_at = models.DateTimeField(auto_now=True)

    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'app_user'
        verbose_name = 'user'
        verbose_name_plural = 'users'

        ordering = ['-created_at']
