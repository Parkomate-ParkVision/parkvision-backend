from users.models import ParkomateUser
from rest_framework import serializers

class ParkomateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkomateUser
        fields = "__all__"