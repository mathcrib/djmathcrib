from django.urls import include, path

from .views import get_article, get_next

urlpatterns = [
    path('', get_next, name="root"),
    path('<int:id>/', get_next, name="get_next"),
    path('<int:id>/read/', get_article, name="article"),
]
