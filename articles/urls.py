from django.urls import path

from .views import (
    ArticleDetailView,
    ArticleCreateView,
    ArticleUpdateView,
    get_next
)

urlpatterns = [
    path('', get_next, name="root"),
    path('<int:pk>/read/', ArticleDetailView.as_view(), name='article_detail'),
    path('add/', ArticleCreateView.as_view(), name='article_create'),
    path(
        'article/<int:pk>/',
        ArticleUpdateView.as_view(),
        name='article_update',
    ),
    path('<int:id>/', get_next, name='get_next'),

]
