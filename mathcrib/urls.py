from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from articles.views import home_page

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('django.contrib.auth.urls')),
    path('articles/', include('articles.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('users/', include('users.urls')),
    path('', home_page, name='home_page'),
]
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT
    )
