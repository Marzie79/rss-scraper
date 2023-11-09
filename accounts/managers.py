from django.apps import apps
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.hashers import make_password


class AllCustomUserManager(BaseUserManager):

    @staticmethod
    def _create_user(email, password, **extra_fields):
        """Create and save a user with the given email, and password.
        
        Args:
            email (str): The entering email for creating an account.
            password (str): The desirable password for creating an account.
        """
        Account = apps.get_model('accounts', 'account')
        account = Account(email=email, **extra_fields)
        account.password = make_password(password)
        account.save()

        return account

    def create_superuser(self, email, password, **extra_fields):
        """Create and super user with the given email, and password.
        
        Args:
            email (str): The entering email for creating a super user.
            password (str): The desirable password for creating a super user.
        """
        extra_fields.setdefault('is_active', 1)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self._create_user(email, password, **extra_fields)


class CustomUserManage(AllCustomUserManager):
    """Custom user manager for filtering user accounts."""

    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)
