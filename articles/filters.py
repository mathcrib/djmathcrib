import re

import django_filters as filters
from django.contrib.auth import get_user_model
from django.db.models import Q

from .models import Article

User = get_user_model()


class ArticleFilter(filters.FilterSet):
    text = filters.CharFilter(method='filter_text')
    author = filters.ModelChoiceFilter(queryset=User.objects.all())
    read_time = filters.RangeFilter()

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
                "') | Q(title__icontains='" + value +"')"
            )
        
        return queryset.filter(
            eval(" | ".join(search), {'__builtins__': None,  'Q': Q}))

    class Meta:
        model = Article
        fields = ['text', 'author', 'read_time']
