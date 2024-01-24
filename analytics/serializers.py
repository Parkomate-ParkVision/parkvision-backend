from rest_framework.serializers import ModelSerializer
from analytics.models import VehicleDetails, PerHourVehicleCount

class VehicleDetailsSerializer(ModelSerializer):
    class Meta:
        model = VehicleDetails
        fields = '__all__'

class PerHourVehicleCountSerializer(ModelSerializer):
    class Meta:
        model = PerHourVehicleCount
        fields = '__all__'