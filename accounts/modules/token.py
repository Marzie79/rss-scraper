from typing import Dict

from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import (RefreshToken, TokenError)

from accounts.models import Account
from utilities.exceptions import MultiLanguageException
from utilities.messages.error import INVALID_TOKEN


def validate_refresh_token(token: str) -> RefreshToken:
    """Validate a string that is a valid refresh token.
    
    Args:
        token (str): The token that we want to validate it.
    
    Returns:
        The instance of RefreshToken that belongs to the input.
    """
    try:
        return RefreshToken(token)
    except TokenError:
        raise MultiLanguageException(INVALID_TOKEN)


def update_token(token: RefreshToken) -> Dict:
    """Create a new refresh and access token for an account.
    
    Returns:
        A dict that has data of a token.

    Example:
        {
            'access_token': 'DZlNfQ.y4lFgRiPe0ul',
            'refresh_token': 'DZlNjg0Y2ExNTUifQ.y4lFgRul'
        }

    """
    if api_settings.ROTATE_REFRESH_TOKENS:

        token.set_jti()
        token.set_exp()

    return to_representation(token)


def block_token(refresh_token: str) -> RefreshToken:
    """Block a token.
    
    Args:
        refresh_token (str): The refresh token that we want to block.

    Returns:
        The RefreshToken instance that is blocked.
    """
    token = validate_refresh_token(refresh_token)
    token.blacklist()

    return token


def to_representation(token: RefreshToken) -> Dict:
    """Represent access and refresh token based RefreshToken instance.
    
    Args:
        token (RefreshToken): The token that we want to present.

    Returns:
        A represent dict of a token.
    """
    return {
        'access_token': str(token.access_token),
        'refresh_token': str(token)
    }


def get_token(account: Account) -> Dict:
    """Get a token for an account.
    
    Args:
        account (Account): The account that we want to generate a token for her.

    Returns:
        A dict of representation of token.
    """
    token = RefreshToken.for_user(account)

    return to_representation(token=token)
