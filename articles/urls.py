from django.urls import path

from .views import (ArticleCreateView, ArticleDetailView, ArticleListView,
                    ArticleSearchListView, ArticleUpdateView, get_next)

urlpatterns = [
    path('navigate/', get_next, name="root"),
    path('navigate/<int:id>/', get_next, name='get_next'),
    path('<int:pk>/read/', ArticleDetailView.as_view(), name='article_detail'),
    path('add/', ArticleCreateView.as_view(), name='article_create'),
    path(
        '<int:pk>/update/',
        ArticleUpdateView.as_view(),
        name='article_update',
    ),
    path('', ArticleListView.as_view(), name='article_list'),
    path('search/', ArticleSearchListView.as_view(), name='search')
    
]
