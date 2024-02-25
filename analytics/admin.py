# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import VehicleDetails


@admin.register(VehicleDetails)
class VehicleDetailsAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'vehicle',
        'owner_name',
        'vehicle_class',
        'norms_type',
        'manufacturer_model',
        'insurance_validity',
        'address',
        'seating_capacity',
        'manufacturing_year',
        'manufacturer',
        'state',
        'fuel_type',
        'puc_valid_upto',
        'insurance_name',
    )
    list_filter = ('vehicle',)
