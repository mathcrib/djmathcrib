from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserRole(models.TextChoices):
    AUTHOR = 'author'
    MODERATOR = 'moderator'


class User(AbstractUser):
    email = models.EmailField(
        _('email'),
        blank=False,
        unique=True,
    )
    role = models.CharField(
        choices=UserRole.choices,
        default=UserRole.AUTHOR,
        max_length=50,
        verbose_name='Роль',
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def is_personal(self):
        return self.role == UserRole.MODERATOR or self.is_superuser


class InvitedUser(models.Model):
    inviting = models.ForeignKey(
        User,
        models.SET_NULL,
        blank=True,
        null=True,
        related_name='inviting',
        verbose_name=_('Пригласивший'),
    )
    invited = models.ForeignKey(
        User,
        models.SET_NULL,
        blank=True,
        null=True,
        related_name='invited',
        verbose_name=_('Приглашенный'),
    )
    created = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Дата приглашения'),
    )
    invite_key = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name=_('Инвайт ключ'),
    )
    invite_url = models.CharField(
        max_length=250,
        blank=True,
        null=True,
        verbose_name=_('Ссылка для регистрации'),
    )

    class Meta:
        ordering = ['-created']
        verbose_name = 'Приглашение'
        verbose_name_plural = 'Приглашения'
