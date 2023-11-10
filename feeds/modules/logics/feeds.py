from typing import List
from uuid import uuid4

import feedparser

from feeds.modules.decorators.mongo import mongo_connection
from feeds.modules.logics.mongo_interface import (store_data, rss_exist)
from utilities.exceptions import MultiLanguageException
from utilities.messages.error import DUPLICATE_RSS


@mongo_connection
def save_feeds(collection, account_id: uuid4, rss: str) -> None:
    """Save fetched feeds for a given account into MongoDB after checking for duplicates.

    Args:
        collection: MongoDB collection to store the feeds.
        account_id (uuid4): The unique identifier for the associated account.
        rss (str): The RSS feed URL to be fetched and processed.
    """

    if rss_exist(collection=collection, account_id=account_id, rss=rss):
        raise MultiLanguageException(DUPLICATE_RSS)

    if feeds := fetch_feeds(account_id=account_id, rss=rss):
        store_data(collection=collection, feeds=feeds)


def __get_value(entity, field: str):
    """Helper function to retrieve a value of a field from an instance.

    Args:
        entity (dict): The instance which to retrieve the field.
        field (str): The field to be retrieved from the entity.

    Returns:
        The value of the field if present, otherwise None.
    """
    return getattr(entity, field) if field in entity else None


def fetch_feeds(account_id: uuid4, rss: str) -> List:
    """Fetches and processes RSS feed entries for a given account.

    Args:
        account_id (uuid4): The unique identifier for the associated account.
        rss (str): The RSS feed URL to be fetched and processed.

    Returns:
        A list of dictionaries containing details of each feed entry..
    """
    result = []
    feeds = feedparser.parse(rss)
    entries = feeds.entries
    entries_details = {
        'rss': rss,
        'account_id': str(account_id),
        'feed_title': __get_value(feeds.feed, 'title'),
        'feed_link': __get_value(feeds.feed, 'link'),
        'feed_updated': __get_value(feeds.feed, 'updated'),
        'feed_modified': __get_value(feeds.feed, 'modified')
    }

    for entry in entries:
        entry_detail = {
            'id':
            __get_value(entry, 'id'),
            'title':
            __get_value(entry, 'title'),
            'link':
            __get_value(entry, 'link'),
            'author':
            __get_value(entry, 'author'),
            'time_published':
            __get_value(entry, 'time_published'),
            'summary':
            __get_value(entry, 'summary'),
            'description':
            __get_value(entry, 'description'),
            'tags':
            [__get_value(tag, 'term')
             for tag in entry.tags] if __get_value(entry, 'tags') else [],
            'authors':
            [__get_value(author, 'name') for author in entry.authors]
            if __get_value(entry, 'authors') else [],
        }

        entry_detail.update(entries_details)
        result.append(entry_detail)

    return result
