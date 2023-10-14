from django.contrib import admin
from .models import Floor, Section, Location
# Register your models here.


class FloorAdmin(admin.ModelAdmin):
    list_display = ('number', 'organization', 'isActive')
    list_filter = ('organization', 'isActive')
    search_fields = ('number', 'organization')


class SectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'floor', 'isActive')
    list_filter = ('floor', 'isActive')
    search_fields = ('name', 'floor')


class LocationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'section', 'isOccupied', 'isAllocated', 'isActive')
    list_filter = ('section', 'isOccupied', 'isAllocated', 'isActive')
    search_fields = ('id', 'name', 'section')

admin.site.register(Floor)
admin.site.register(Section)
admin.site.register(Location)