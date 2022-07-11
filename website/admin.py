from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import *
from .forms import *

class UserAdmin1(UserAdmin):
    add_form = UserCreationForm1
    form = UserChangeForm1
    model = User
    list_display = ["username", "email"]
    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        ('Public info', {
            'fields': ('description', 'owns', 'coin', 'materia')
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'email')
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions'
                )
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        })
    )

admin.site.register(User, UserAdmin1)
admin.site.register(Item)