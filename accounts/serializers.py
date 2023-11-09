from rest_framework import serializers


class TokenRefreshSerializer(serializers.Serializer):
    """Validate refresh token data."""
    refresh_token = serializers.CharField()


class AuthenticationSerializer(serializers.Serializer):
    """Validate authentication data."""
    email = serializers.EmailField()
    password = serializers.CharField()
