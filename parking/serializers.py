from rest_framework import serializers
from .models import Parking, CCTV


class ParkingSerializer(serializers.ModelSerializer):
    organizationName = serializers.SerializerMethodField()
    class Meta:
        model = Parking
        fields = ['id', 'organization', 'name', 'totalSlots', 'availableSlots', 'isActive', 'organizationName']
    
    def get_organizationName(self, obj):
        return obj.organization.name
    
    
class CCTVSerializer(serializers.ModelSerializer):
    parkingName = serializers.SerializerMethodField()
    class Meta:
        model = CCTV
        fields = ['id', 'parking', 'name', 'url', 'isActive', 'parkingName']
    
    def get_parkingName(self, obj):
        return obj.parking.name