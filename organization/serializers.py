from organization.models import (
    Organization,
    Gate
)
from rest_framework import serializers
from users.models import ParkomateUser


class OrganizationSerializer(serializers.ModelSerializer):
    ownerName = serializers.SerializerMethodField()
    adminDetails = serializers.SerializerMethodField()

    class Meta:
        model = Organization
        fields = [
            'id',
            'name',
            'owner',
            'address',
            'entry_gates',
            'exit_gates',
            'total_slots',
            'filled_slots',
            'parking_threshold',
            'hourly_rate',
            'occupancy_limit',
            'penalty_charges',
            'createdAt',
            'updatedAt',
            'isActive',
            'admins',
            'adminDetails',
        ]
        get_fields = fields.append('ownerName')
        list_fields = fields.append('ownerName')

    def get_adminDetails(self, obj):
        admins = obj.admins
        if admins is None:
            return "No Admins Found"
        final_data = []
        for count, email in enumerate(admins):
            data = {}
            data['email'] = email
            adminObj = ParkomateUser.objects.filter(email=email)
            if adminObj.exists():
                adminObj = adminObj.first()
                data['phone'] = str(adminObj.phone)
                data['name'] = str(adminObj.name)
                data['id'] = count
            final_data.append(data)
        return final_data

    def get_ownerName(self, obj):
        if obj.owner:
            return obj.owner.name
        return "no owner found"


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
