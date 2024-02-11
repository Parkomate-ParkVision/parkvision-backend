from users.models import ParkomateUser
from rest_framework import serializers
from django.contrib import auth
from rest_framework.serializers import CharField, SerializerMethodField, ModelSerializer, Serializer
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError


class ParkomateUserSerializer(ModelSerializer):
    class Meta:
        model = ParkomateUser
        fields = "__all__"


class RegisterSerializer(ModelSerializer):
    password = CharField()

    class Meta:
        model = ParkomateUser
        fields = ['name', 'email', 'phone', 'password']

    def create(self, validated_data):
        return ParkomateUser.objects.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):
    email = CharField(max_length=255, min_length=3)
    password = CharField(write_only=True)
    tokens = SerializerMethodField()

    def get_tokens(self, obj):
        user = ParkomateUser.objects.get(email=obj['email'])
        return {
            'refresh': user.tokens()['refresh'],
            'access': user.tokens()['access']
        }

    class Meta:
        model = ParkomateUser
        fields = ['id', 'email', 'name',
                  'profilePicture', 'password', 'tokens']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        user: ParkomateUser = auth.authenticate(email=email, password=password)
        if not user:
            raise AuthenticationFailed(
                'Invalid credentials, please try again!')
        if not user.is_active:
            raise AuthenticationFailed(
                'Account disabled, please contact admin!')
        return {
            'id': user.id,
            'email': user.email,
            'profilePicture': user.profilePicture,
            'name': user.name,
            'tokens': user.tokens
        }


class LogoutSerializer(Serializer):
    refresh = CharField()

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            refresh_token = RefreshToken(self.token)
            refresh_token.blacklist()
        except TokenError:
            self.fail('bad_token')
