from django.contrib import admin
from django.urls import include, path

from articles.views import home_page

urlpatterns = [
    path('admin/', admin.site.urls),
    path('articles/', include('articles.urls')),
    path('', home_page, name='home_page'),
]
