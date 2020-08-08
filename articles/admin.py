from django.contrib import admin
from django.db import models
from martor.widgets import AdminMartorWidget

from .models import Article


class ArticleAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': AdminMartorWidget},
    }
    list_display = ("pk", "title", "text", "parent", "author", "created", "updated")
    search_fields = ("text",)
    list_filter = ("created", "author")
    empty_value_display = "-пусто-"


admin.site.register(Article, ArticleAdmin)
