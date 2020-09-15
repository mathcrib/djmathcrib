import re

from django import forms
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

import django_filters as filters

from .models import Article

User = get_user_model()

ARTICLE_LENGTH = (
    (0, _("до 5 минут")),
    (1, _("5-10 минут")),
    (2, _("более 10 минут")),
)


class ArticleFilter(filters.FilterSet):
    text = filters.CharFilter(method='filter_text', widget=forms.TextInput(attrs={"type": "search", "placeholder": "Поиск"}))
    author = filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        empty_label='все',
    )
    read_time = filters.ChoiceFilter(
        choices=ARTICLE_LENGTH,
        empty_label='любое',
        method='filter_read_time',
    )
    separate = filters.BooleanFilter(
        widget=forms.CheckboxInput,
        label='Искать отдельно каждое слово',
        method='filter_none',
    )

    def filter_none(self, queryset, name, value):
        return queryset

    def filter_read_time(self, queryset, name, value):
        if value == "0":
            return queryset.filter(read_time__lt=5)
        elif value == "1":
            return queryset.filter(read_time__gte=5, read_time__lte=10)
        elif value == "2":
            return queryset.filter(read_time__gt=10)
        return queryset

    def filter_text(self, queryset, name, value):
        separate = self.request.GET.get('separate', None)

        if separate is None:
            values = [value]
        else:
            values = re.sub("[^\w]", " ", value).split()

        search = []
        for value in values:
            search.append(
                "Q(text__icontains='" + value +
                "') | Q(title__icontains='" + value + "')"
            )

        return queryset.filter(
            eval(" | ".join(search), {'__builtins__': None, 'Q': Q}))

    class Meta:
        model = Article
        fields = ['text', 'author', 'read_time']
