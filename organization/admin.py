# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Organization, Gate


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'owner',
        'admins',
        'name',
        'address',
        'entry_gates',
        'exit_gates',
        'total_slots',
        'filled_slots',
        'createdAt',
        'updatedAt',
        'isActive',
    )
    list_filter = ('owner', 'createdAt', 'updatedAt', 'isActive')
    search_fields = ('name',)


@admin.register(Gate)
class GateAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'organization',
        'createdAt',
        'updatedAt',
        'isActive',
    )
    list_filter = ('organization', 'createdAt', 'updatedAt', 'isActive')
