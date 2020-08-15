from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from mptt.admin import DraggableMPTTAdmin

from .models import Article


class MyDraggableMPTTAdmin(DraggableMPTTAdmin):
    list_display = ('tree_actions', 'something')
    list_display_links = ('something',)

    def something(self, instance):
        return format_html(
            '<div style="text-indent:{}px">{}</div>',
            instance._mpttfield('level') * self.mptt_level_indent,
            instance.title,
        )
    something.short_description = _('Название раздела или статьи')


admin.site.register(
    Article,
    MyDraggableMPTTAdmin,
    list_display=(
        'tree_actions',
        'something',
        'is_published',
        'is_category',
    ),
    list_display_links=(
        'something',
    ),
)
