from django.contrib import admin
from .models import Organization, Gate, Vehicle

class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'entry_gates', 'exit_gates', 'total_slots', 'filled_slots')
    search_fields = ('name', 'address')
    list_filter = ('entry_gates', 'exit_gates', 'total_slots', 'filled_slots')

class GateAdmin(admin.ModelAdmin):
    list_display = ('id', 'organization')
    list_filter = ('organization',)
    search_fields = ('id',)

class VehicleAdmin(admin.ModelAdmin):
    list_display = ('number_plate', 'prediction', 'entry_gate', 'exit_gate', 'entry_time', 'exit_time')
    list_filter = ('entry_gate', 'exit_gate')
    search_fields = ('number_plate', 'prediction')

admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Gate, GateAdmin)
admin.site.register(Vehicle, VehicleAdmin)