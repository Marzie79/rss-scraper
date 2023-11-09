from rest_framework.response import Response
from rest_framework import (status, permissions, generics)

from accounts.modules.account import (authenticate, logout, refresh)
from accounts.serializers import (AuthenticationSerializer,
                                  TokenRefreshSerializer)


class TokenRefreshView(generics.GenericAPIView):
    """Update refresh and access token of an account."""
    permission_classes = [permissions.AllowAny]
    serializer_class = TokenRefreshSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(data=refresh(
            serializer.validated_data['refresh_token']),
                        status=status.HTTP_200_OK)


class LogoutView(generics.GenericAPIView):
    """Logout an account with blocking her current token."""
    serializer_class = TokenRefreshSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        logout(serializer.validated_data['refresh_token'])

        return Response(status=status.HTTP_200_OK)


class AuthenticationView(generics.GenericAPIView):
    """Login an existing account or signup a new account."""
    permission_classes = [permissions.AllowAny]
    serializer_class = AuthenticationSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(data=authenticate(**serializer.validated_data),
                        status=status.HTTP_200_OK)
