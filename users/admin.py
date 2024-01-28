# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import ParkomateUser


@admin.register(ParkomateUser)
class ParkomateUserAdmin(admin.ModelAdmin):
    list_display = (
        'password',
        'last_login',
        'id',
        'name',
        'email',
        'phone',
        'profilePicture',
        'privilege',
        'is_active',
        'is_admin',
        'is_staff',
        'is_superuser',
    )
    list_filter = (
        'last_login',
        'is_active',
        'is_admin',
        'is_staff',
        'is_superuser',
    )
    raw_id_fields = ('groups', 'user_permissions')
    search_fields = ('name',)
