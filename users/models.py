from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    AUTHOR = 'author'
    MODERATOR = 'moderator'

    ROLE_CHOICES = [
        (AUTHOR, 'Автор'),
        (MODERATOR, 'Модератор'),
    ]

    role = models.CharField(
        choices=ROLE_CHOICES,
        default=AUTHOR,
        max_length=50,
        verbose_name='Роль',
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
