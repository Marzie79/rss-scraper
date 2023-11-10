import datetime
from uuid import uuid4

from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models

from accounts.managers import (CustomUserManage, AllCustomUserManager)


class Account(AbstractBaseUser):

    class IsActiveChoices(models.IntegerChoices):
        ACTIVE = 1
        NOT_ACTIVE = 0
        PENDING = 2

    id = models.UUIDField(default=uuid4,
                          primary_key=True,
                          unique=True,
                          help_text='Unique identifier for the user account.')
    email = models.EmailField(
        unique=True, help_text='Email address used for user identification.')
    is_superuser = models.BooleanField(
        default=False,
        help_text='Indicates whether the user has superuser privileges.')
    is_staff = models.BooleanField(
        default=False,
        help_text='Indicates whether the user has staff privileges.')
    is_active = models.IntegerField(default=IsActiveChoices.ACTIVE.value,
                                    choices=IsActiveChoices.choices,
                                    help_text='User account status')
    date_joined = models.DateTimeField(
        auto_now_add=True, help_text='Time when the user account was created.')
    is_deleted = models.BooleanField(
        default=False,
        help_text='Indicates whether the user account is deleted.')
    deletion_date = models.DateTimeField(
        null=True,
        blank=True,
        editable=False,
        help_text='Time when the user account was deleted')

    objects = CustomUserManage()
    all_objects = AllCustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'account'

    def __str__(self):
        return self.email

    def delete(self, force_delete=False, *args, **kwargs):
        """Soft delete the user account if force_delete is not True."""
        if force_delete:
            super().delete(*args, **kwargs)
        else:
            self.is_deleted = True
            self.deletion_date = datetime.datetime.now()
            self.save(force_update=True)

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser
