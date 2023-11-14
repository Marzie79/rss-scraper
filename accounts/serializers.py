import re

from rest_framework import serializers

from utilities.exceptions import MultiLanguageException
from utilities.messages.error import WEAK_PASSWORD


class TokenRefreshSerializer(serializers.Serializer):
    """Validate refresh token data."""
    refresh_token = serializers.CharField()


class AuthenticationSerializer(serializers.Serializer):
    """Validate authentication data."""
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate_password(self, value: str):
        """Validate that the entered password is strong."""
        if not re.match(
                "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$",
                value):
            raise MultiLanguageException(WEAK_PASSWORD)
