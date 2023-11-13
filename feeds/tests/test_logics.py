from unittest.mock import patch
from uuid import uuid4

import mongomock
from bson import ObjectId
from django.test import TestCase

from utilities.exceptions import MultiLanguageException


def mock_decorator(func):

    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


patch('feeds.modules.decorators.mongo.mongo_connection',
      mock_decorator).start()
from feeds.modules.logics.mongo_interface import (add_bookmark, save_feeds,
                                                  get_account_feeds,
                                                  add_comment)


class TestFeeds(TestCase):
    """Test cases for the functions related to feeds."""

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

    def test_save_feeds_green(self):
        """Test saving feeds successfully."""
        account_id = uuid4()

        save_feeds(self.mock_collection, account_id, self.fixture_rss)

        inserted_data = self.mock_collection.find_one({
            'account_id':
            str(account_id),
            'rss':
            self.fixture_rss
        })

        self.assertIsNotNone(inserted_data)

    def test_save_feeds_red(self):
        """Test attempting to save duplicate feeds, expecting an exception."""
        account_id = uuid4()
        save_feeds(self.mock_collection, account_id, self.fixture_rss)

        with self.assertRaises(MultiLanguageException):
            save_feeds(self.mock_collection, account_id, self.fixture_rss)

    def test_add_bookmark_green(self):
        """Test adding a bookmark to an existing entry successfully."""
        id_ = '5f77c6d132e41f17b0a5b6ec'
        account_id = uuid4()
        data = [{'_id': ObjectId(id_), 'account_id': str(account_id)}]

        self.mock_collection.insert_many(data)

        add_bookmark(self.mock_collection, id_, account_id)

        updated_document = self.mock_collection.find_one({
            '_id':
            ObjectId(id_),
            'account_id':
            str(account_id)
        })

        self.assertIsNotNone(updated_document)
        self.assertTrue(updated_document.get('bookmark'))

    def test_add_bookmark_red(self):
        """Test attempting to add a bookmark to a non-existing entry, expecting an exception."""
        id_ = '5f77c6d132e41f17b0a5b6ec'

        with self.assertRaises(MultiLanguageException):
            add_bookmark(self.mock_collection, id_, uuid4())

    def test_add_comment_green(self):
        """Test adding a comment on an existing entry successfully."""
        id_ = '5f77c6d132e41f17b0a766ec'
        account_id = uuid4()
        data = [{'_id': ObjectId(id_), 'account_id': str(account_id)}]
        comment = 'This is my comment.'

        self.mock_collection.insert_many(data)

        add_comment(self.mock_collection, id_, account_id, comment)

        updated_document = self.mock_collection.find_one({
            '_id':
            ObjectId(id_),
            'account_id':
            str(account_id),
        })

        self.assertIsNotNone(updated_document)
        self.assertTrue(updated_document.get('comment'))

    def test_add_comment_red(self):
        """Test attempting to add a comment on a non-existing entry, expecting an exception."""
        id_ = '5f77c6d132e41f17b0a5b6ec'
        comment = 'This is my comment.'

        with self.assertRaises(MultiLanguageException):
            add_comment(self.mock_collection, id_, uuid4(), comment)

    def test_get_account_feeds_green(self):
        """Test retrieving feeds for an account successfully."""
        account_id = uuid4()

        save_feeds(self.mock_collection, account_id, self.fixture_rss)

        feeds = get_account_feeds(self.mock_collection, 1, 10, account_id)

        self.assertIsNotNone(feeds)
        self.assertEqual(feeds[0]['account_id'], str(account_id))
