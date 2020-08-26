import readtime
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from mptt.managers import TreeManager
from mptt.models import MPTTModel, TreeForeignKey

User = get_user_model()


class ArticleModelManager(TreeManager):
    """
    Кастомный менеджер запросов к БД.
    """

    def published(self):
        """
        Возвращает queryset c опубликованными сущностями: категории, статьи.
        """
        return self.filter(is_published=True)

    def get_category(self):
        """
        Возвращает queryset, содержащий только опубликованные категории.
        """
        return self.filter(is_published=True, is_category=False)

    def get_articles(self):
        """
        Возвращает queryset, содержащий только опубликованные статьи.
        """
        return self.filter(is_published=True, is_category=False)


class Article(MPTTModel):
    title = models.CharField(
        max_length=150,
        verbose_name=_('Название'),
        unique=True
    )
    text = RichTextUploadingField(
        verbose_name=_('Текст статьи'),
        null=True,
        blank=True,
    )
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
    read_time = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        verbose_name=_('Время чтения статьи'),
    )
    is_published = models.BooleanField(
        default=False,
        verbose_name=_('Опубликована'),
    )
    is_category = models.BooleanField(
        default=False,
        verbose_name=_('Категория'),
    )

    objects = ArticleModelManager()

    class Meta:
        verbose_name = _('cтатья')
        verbose_name_plural = _('cтатьи')

    class MPTTMeta:
        order_insertion_by = ('title',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article_detail', kwargs={'pk': self.id})

    def get_full_read_time(self):
        last_dig = self.read_time % 10
        if last_dig == 1:
            min = " минута"
        elif last_dig in [2, 3, 4]:
            min = " минуты"
        else: 
            min = " минут"
        return str(self.read_time) + min

    def save(self, *args, **kwargs):
        if not self.is_category:
            self.read_time = readtime.of_text(self.text).minutes
        return super().save(*args, **kwargs)
