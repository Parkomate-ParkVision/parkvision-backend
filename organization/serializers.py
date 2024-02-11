from organization.models import (
    Organization,
    Gate
)
from rest_framework import serializers
from users.models import ParkomateUser


class OrganizationSerializer(serializers.ModelSerializer):
    ownerName = serializers.SerializerMethodField()
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
            'isActive',
        ]
        get_fields = fields.append('ownerName')
        list_fields = fields.append('ownerName')
    
    def create(self, validated_data):
        user = self.context['request'].user
        print(user)
        owner = ParkomateUser.objects.get(id=user.id)
        validated_data['owner'] = owner
        return super().create(validated_data)

    def get_ownerName(self, obj):
        return obj.owner.name

class GateSerializer(serializers.ModelSerializer):
    organizationName = serializers.SerializerMethodField()
    organizationAddress = serializers.SerializerMethodField()

    class Meta:
        model = Gate
        fields = [
            'id',
            'organization',
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
