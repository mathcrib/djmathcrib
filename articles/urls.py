from django.urls import path

from . import views

urlpatterns = [
    path('navigate/', views.get_next, name="root"),
    path('navigate/<int:id>/', views.get_next, name='get_next'),
    path(
        '<int:pk>/read/', 
        views.ArticleDetailView.as_view(), 
        name='article_detail'
    ),
    path('add/', views.ArticleCreateView.as_view(), name='article_create'),
    path(
        '<int:pk>/update/',
        views.ArticleUpdateView.as_view(),
        name='article_update',
    ),
    path(
        'search/', 
        views.ArticleListView.as_view(), 
        name='search'
    ),
    
]
