from typing import Dict

from accounts.models import Account
from accounts.modules.token import (get_token, block_token, update_token)
from utilities.exceptions import MultiLanguageException
from utilities.messages.error import INVALID_PASSWORD


def logout(refresh_token: str) -> None:
    """Logout an account with blocking her refresh token.
    
    Args:
        refresh_token (str): The token that we want to block.
    """
    block_token(refresh_token=refresh_token)


def refresh(refresh_token: str) -> Dict:
    """Refresh new tokens for an account.
    
    Args:
        refresh_token (str): The refresh token that we want to rotate.

    Returns:
        The new tokens of an account.
    """
    token = block_token(refresh_token=refresh_token)
    return update_token(token=token)


def authenticate(email: str, password: str) -> Dict:
    """Authenticate an account with her email and password.
    
        If the email does not exist, we create a new account for this email.

    Args:
        email (str): The email of account for authentication.
        password (str): The password of account for authentication.

    Returns:
        The dict of tokens of an account.
    """
    try:
        account = Account.objects.get(email=email)
    except Account.DoesNotExist:
        account = Account.objects.create(email=email)
        account.set_password(raw_password=password)
        account.save(update_fields=['password'])

        return get_token(account)

    if account.check_password(raw_password=password):
        return get_token(account=account)

    raise MultiLanguageException(INVALID_PASSWORD)
