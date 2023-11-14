from django.test import TestCase

from utilities.exceptions import MultiLanguageException
from accounts.modules.account import (authenticate, refresh, logout)
from accounts.modules.token import validate_refresh_token


class TestFeeds(TestCase):
    """Test cases for the functions related to authentication."""

    @classmethod
    def setUpClass(cls):
        """Set up common fixture data for all test cases."""
        cls.fixture_email = 'marzie.7900@gmail.com'
        cls.fixture_password = '456fghj^$J'
        super().setUpClass()

    def test_sign_in_green(self):
        """Test successful user authentication."""
        authenticate(self.fixture_email, self.fixture_password)
        tokens = authenticate(self.fixture_email, self.fixture_password)

        self.assertEqual(['access_token', 'refresh_token'],
                         list(tokens.keys()))

    def test_sign_in_red(self):
        """Test authentication failure with incorrect password."""
        authenticate(self.fixture_email, self.fixture_password)

        with self.assertRaises(MultiLanguageException):
            authenticate(self.fixture_email, self.fixture_password[:1])

    def test_refresh_green(self):
        """Test successful token refresh."""
        tokens = authenticate(self.fixture_email, self.fixture_password)

        new_tokens = refresh(tokens['refresh_token'])

        self.assertNotEqual(tokens['access_token'], new_tokens['access_token'])
        self.assertNotEqual(tokens['refresh_token'],
                            new_tokens['refresh_token'])

    def test_logout_green(self):
        """Test successful user logout and token invalidation."""
        tokens = authenticate(self.fixture_email, self.fixture_password)

        logout(tokens['refresh_token'])

        with self.assertRaises(MultiLanguageException):
            validate_refresh_token(tokens['refresh_token'])
