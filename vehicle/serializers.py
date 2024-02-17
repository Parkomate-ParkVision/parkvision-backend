from vehicle.models import (
    Vehicle
)
from rest_framework import serializers


class VehicleSerializer(serializers.ModelSerializer):
    admin_name = serializers.SerializerMethodField()
    admin_email = serializers.SerializerMethodField()
    admin_organization = serializers.SerializerMethodField()
    parking_name = serializers.SerializerMethodField()
    class Meta:
        model = Vehicle
        fields = [
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
            'admin_name',
            'admin_email',
            'admin_organization',
            'parking',
            'parking_name',
        ]
        get_fields = fields
        post_fields = fields

    def get_admin_name(self, obj):
        return obj.verified_by.name if obj.verified_by else "Not Verified"
    
    def get_admin_email(self, obj):
        return obj.verified_by.email if obj.verified_by else "Not Verified"
    
    def get_admin_organization(self, obj):
        return obj.entry_gate.organization.name
    
    def get_parking_name(self, obj):
        return obj.parking.name if obj.parking else "Not Parked"