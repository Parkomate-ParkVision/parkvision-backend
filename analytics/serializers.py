from rest_framework.serializers import ModelSerializer, Serializer, CharField
from analytics.models import VehicleDetails


class VehicleDetailsSerializer(ModelSerializer):
    class Meta:
        model = VehicleDetails
        fields = [
            'id',
            'vehicle',
            'owner_name',
            'vehicle_class',
            'norms_type',
            'manufacturer_model',
            'insurance_validity',
            'address',
            'seating_capacity',
            'manufacturing_year',
            'manufacturer',
            'state',
            'fuel_type',
            'puc_valid_upto',
            'insurance_name'
        ]
        list_fields = fields
        get_fields = fields

class IDFYRequestSerializer(Serializer):
    rc_number = CharField()
    challan_blacklist_details = CharField()
    vehicle = CharField()