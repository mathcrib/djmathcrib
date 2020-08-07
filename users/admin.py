from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from .models import User


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('id', 'email', 'username', 'role')


admin.site.register(User, CustomUserAdmin)
admin.site.unregister(Group)
