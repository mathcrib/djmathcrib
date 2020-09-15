from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from ckeditor_uploader.fields import RichTextUploadingField

User = get_user_model()


class Campaign(models.Model):
    from_email = models.EmailField(
        default=settings.PROJECT_EMAIL,
        verbose_name=_('От кого'),
    )
    to_emails = models.ManyToManyField(
        User,
        verbose_name=_('Кому'),
        blank=True,
        null=True,
    )
    subject = models.CharField(
        max_length=250,
        unique=True,
        verbose_name=_('Название'),
    )
    html_content = RichTextUploadingField(
        verbose_name=_('Текст'),
        null=True,
        blank=True,
    )
