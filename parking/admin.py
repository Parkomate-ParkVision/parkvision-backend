# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Parking, CCTV


@admin.register(Parking)
class ParkingAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'organization',
        'name',
        'totalSlots',
        'availableSlots',
        'isActive',
    )
    list_filter = ('organization', 'isActive')
    search_fields = ('name',)


@admin.register(CCTV)
class CCTVAdmin(admin.ModelAdmin):
    list_display = ('id', 'parking', 'name', 'url', 'isActive')
    list_filter = ('parking', 'isActive')
    search_fields = ('name',)
