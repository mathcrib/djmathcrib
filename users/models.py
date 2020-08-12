from django.contrib.auth.models import AbstractUser
from django.db import models


class UserRole(models.TextChoices):
    AUTHOR = 'author'
    MODERATOR = 'moderator'


class User(AbstractUser):
    role = models.CharField(
        choices=UserRole.choices,
        default=UserRole.AUTHOR,
        max_length=50,
        verbose_name='Роль',
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
