from api.models import (
    Organization,
    Gate,
    Vehicle
)
from rest_framework import serializers

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = "__all__"

class GateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gate
        fields = "__all__"

class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = "__all__"