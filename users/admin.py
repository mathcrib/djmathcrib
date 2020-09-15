from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from .models import InvitedUser, User


class CustomUserAdmin(BaseUserAdmin):
    model = User
    list_display = ('id', 'email', 'username', 'role')


class UserAdmin(BaseUserAdmin):

    list_display = ('username', 'email', 'role')
    list_filter = ('role',)
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Персональная информация', {
            'fields': ('first_name', 'last_name', 'telegram')
        }),
        ('Роль на сайте', {'fields': ('role', 'is_superuser')}),
    )

    search_fields = ('email', 'username')
    ordering = ('username',)


class InvitedUserAdmin(admin.ModelAdmin):
    list_display = ('inviting', 'invited', 'created', 'invite_url')
    search_fields = ('invited',)
    list_filter = ('created',)
    empty_value_display = '-пусто-'


admin.site.register(InvitedUser, InvitedUserAdmin)
admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
