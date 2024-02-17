# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Vehicle


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'number_plate',
        'cropped_image',
        'vehicle_image',
        'entry_gate',
        'exit_gate',
        'entry_time',
        'exit_time',
        'verified_by',
        'verified_number_plate',
        'parking',
    )
    list_filter = ('entry_time', 'exit_time')
    raw_id_fields = ('entry_gate', 'exit_gate')
