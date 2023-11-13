from unittest.mock import patch
from uuid import uuid4

import mongomock
from django.test import TestCase


def mock_decorator(func):

    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


patch('feeds.modules.decorators.mongo.mongo_connection',
      mock_decorator).start()
from feeds.modules.logics.mongo_interface import save_feeds
from feeds.modules.tasks.feeds import update_feeds


class TestFeedsTask(TestCase):
    """Test cases for the functions related to feeds task."""

    @classmethod
    def setUpClass(cls):
        """Setup some fixture data to use in all test cases."""
        super().setUpClass()
        mock_client = mongomock.MongoClient()
        mock_db = mock_client['rss-scraper']
        cls.mock_collection = mock_db['feed']
        cls.fixture_rss = 'https://www.nasa.gov/rss/dyn/breaking_news.rss'

    @classmethod
    def tearDownClass(cls):
        """Stop mocking the MongoDB connection decorator after all test cases."""
        patch('feeds.modules.decorators.mongo.mongo_connection',
              mock_decorator).stop()
        super().tearDownClass()

    def test_update_feeds_green(self):
        """Test updating feeds successfully."""
        account_id = uuid4()

        save_feeds(self.mock_collection, account_id, self.fixture_rss)

        self.mock_collection.insert_many([{
            'account_id': str(account_id),
            'rss': self.fixture_rss,
            'parent_updated': 'test'
        }, {
            'account_id': str(uuid4()),
            'rss': 'wrong_data',
            'parent_updated': 'test'
        }])

        update_feeds(self.mock_collection)
