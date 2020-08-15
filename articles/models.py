from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey

from .templatetags.read_time import read

User = get_user_model()


class Article(MPTTModel):
    title = models.CharField(
        max_length=150,
        verbose_name=_('Название'),
        unique=True
    )
    text = RichTextUploadingField(verbose_name=_('Текст статьи'), null=True, blank=True)
    author = models.ForeignKey(
        User,
        models.SET_NULL,
        blank=True,
        null=True,
        related_name='articles',
        verbose_name=_('Автор'),
    )
    created = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Дата создания')
    )
    updated = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Дата последнего изменения')
    )
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name=_('Родительский раздел')
    )
    read_time = models.CharField(max_length=50, blank=True, null=True,)

    class Meta:
        verbose_name = _('cтатья')
        verbose_name_plural = _('cтатьи')

    class MPTTMeta:
        order_insertion_by = ('title',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article_detail', kwargs={'pk': self.id})

    def save(self, *args, **kwargs):
        if self.text:
            self.read_time = read(self.text)
        return super().save(*args, **kwargs)
