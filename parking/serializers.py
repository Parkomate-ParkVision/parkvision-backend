from rest_framework import serializers
from .models import Floor, Section, Location

class FloorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Floor
        fields = ['number', 'organization']
    
class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ['name', 'floor']

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'name', 'section', 'isOccupied', 'isAllocated', 'isActive']