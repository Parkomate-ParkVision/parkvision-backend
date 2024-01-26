from organization.models import (
    Organization,
    Gate
)
from rest_framework import serializers


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = [
            'id',
            'name',
            'address',
            'entry_gates',
            'exit_gates',
            'total_slots',
            'filled_slots',
            'createdAt',
            'updatedAt',
            'isActive'
        ]
        get_fields = fields
        list_fields = fields


class GateSerializer(serializers.ModelSerializer):
    organizationName = serializers.SerializerMethodField()
    organizationAddress = serializers.SerializerMethodField()

    class Meta:
        model = Gate
        fields = [
            'id',
            'organization'
            'organizationName',
            'organizationAddress',
            'createdAt',
            'updatedAt',
            'isActive'
        ]

    def get_organizationName(self, obj):
        return obj.organization.name

    def get_organizationAddress(self, obj):
        return obj.organization.address
