from django.urls import path

from accounts.views import (LogoutView, AuthenticationView, TokenRefreshView)

urlpatterns = [
    path('logout/', LogoutView.as_view(), name='logout'),
    path('refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('authentication/', AuthenticationView.as_view(), name='authentication'),
]
