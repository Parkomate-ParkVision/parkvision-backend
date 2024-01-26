from vehicle.models import (
    Vehicle
)
from rest_framework import serializers


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = [
            'id',
            'number_plate',
            'cropped_image',
            'vehicle_image',
            'prediction',
            'entry_gate',
            'exit_gate',
            'entry_time',
            'exit_time',
        ]
        get_fields = fields
        post_fields = fields
