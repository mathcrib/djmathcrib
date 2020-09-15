from django.urls import path

from django_filters.views import FilterView

from .filters import ArticleFilter
from .views import (
    ArticleCreateView,
    ArticleDetailView,
    ArticleListView,
    ArticleUpdateView
)

urlpatterns = [
    path('<int:pk>/read/', ArticleDetailView.as_view(), name='article_detail'),
    path('add/', ArticleCreateView.as_view(), name='article_create'),
    path(
        '<int:pk>/update/',
        ArticleUpdateView.as_view(),
        name='article_update',
    ),
    path('', ArticleListView.as_view(), name='article_list'),
    path(
        'search/',
        FilterView.as_view(filterset_class=ArticleFilter),
        name='search',
    ),
]
