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
            return queryset.filter(
                Q(text__icontains=value) | Q(title__icontains=value)
            )
        print(value)
        ids = set()
        for word in name.split():
            query = set(queryset.filter(
                Q(text__icontains=value) | Q(title__icontains=value)
                ).values_list('pk', flat=True))
            ids = ids.union(query)
        return queryset.filter(pk__in=ids)

    class Meta:
        model = Article
        fields = ['text', 'author', 'read_time']
