from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from martor.models import MartorField
from mptt.models import MPTTModel, TreeForeignKey

User = get_user_model()


class Article(MPTTModel):
    title = models.CharField(
        max_length=150, 
        verbose_name=_('Название'), 
        unique=True
    )
    text = MartorField(
        verbose_name=_('Текст статьи'), 
        null=True, 
        blank=True
    )
    author = models.ForeignKey(
        User, 
        models.SET_NULL, 
        related_name='articles', 
        verbose_name=_('Автор'), 
        null=True, 
        blank=True
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
    

    class Meta:
        verbose_name = _('статья')
        verbose_name_plural = _('статьи')
    
    class MPTTMeta:
        order_insertion_by = ['title']
