from uuid import uuid4
from typing import List

from bson.objectid import ObjectId

from feeds.modules.decorators.mongo import mongo_connection
from feeds.modules.logics.feeds import fetch_feeds
from utilities.exceptions import MultiLanguageException
from utilities.messages.error import (INVALID_ENTRY_ID, DUPLICATE_RSS)


def __representation(feeds) -> List:
    """Convert MongoDB feed data representation for serialization.

    Args:
        feeds: MongoDB feed data.

    Returns:
        A list of feed entries with desirable format.
    """
    result = []

    for entry in feeds:
        entry['_id'] = str(entry['_id'])
        result.append(entry)

    return result


def __rss_exist(collection, account_id: uuid4, rss: str) -> bool:
    """Check if a specific RSS feed already exists for a given account.

    Args:
        collection: MongoDB collection to query.
        account_id (uuid4): The unique identifier for the associated account.
        rss (str): The RSS feed URL to check for existence.

    Returns:
        True if the RSS feed exists, False otherwise.
    """
    return True if collection.find_one({
        'account_id': str(account_id),
        'rss': rss
    }) else False


def __store_data(collection, feeds: List) -> None:
    """Store feed data in the specified MongoDB collection.

    Args:
        collection: MongoDB collection to store the feed data.
        feeds (list): List of dictionaries representing feed entries.
    """
    collection.insert_many(feeds)


@mongo_connection
def save_feeds(collection, account_id: uuid4, rss: str) -> None:
    """Save fetched feeds for a given account into MongoDB after checking for duplicates.

    Args:
        collection: MongoDB collection to store the feeds.
        account_id (uuid4): The unique identifier for the associated account.
        rss (str): The RSS feed URL to be fetched and processed.
    """

    if __rss_exist(collection=collection, account_id=account_id, rss=rss):
        raise MultiLanguageException(DUPLICATE_RSS)

    if feeds := fetch_feeds(account_id=account_id, rss=rss):
        __store_data(collection=collection, feeds=feeds)


@mongo_connection
def add_bookmark(collection,
                 id: str,
                 account_id: uuid4,
                 bookmark: bool = True):
    """Update the bookmark status for a specific entry in the MongoDB collection.

    Args:
        collection: MongoDB collection to update.
        id (str): The ObjectId of the entry to be updated.
        account_id (uuid4): The unique identifier for the associated account.
        bookmark (bool): The bookmark status to set.
    """
    result = collection.update_one(
        {
            '_id': ObjectId(id),
            'account_id': str(account_id),
        }, {'$set': {
            'bookmark': bookmark
        }})

    if not result.matched_count:
        raise MultiLanguageException(INVALID_ENTRY_ID)


@mongo_connection
def add_comment(collection, id: str, account_id: uuid4, comment: str):
    """Update the bookmark status for a specific entry in the MongoDB collection.

    Args:
        collection: MongoDB collection to update.
        id (str): The ObjectId of the entry to be updated.
        account_id (uuid4): The unique identifier for the associated account.
        comment (str): The comment of user for a feed..
    """
    result = collection.update_one(
        {
            '_id': ObjectId(id),
            'account_id': str(account_id),
        }, {'$set': {
            'comment': comment
        }})

    if not result.matched_count:
        raise MultiLanguageException(INVALID_ENTRY_ID)


@mongo_connection
def get_account_feeds(collection, limit: int, offset: int,
                      account_id: uuid4) -> List:
    """Retrieve paginated feed data for a specific account.

    Args:
        collection: MongoDB collection to query.
        limit (int): The number of feed entries to retrieve per page.
        offset (int): The page number to retrieve, with the first page being 1.
        account_id (uuid4): The unique identifier for the associated account.

    Returns:
        A list of feed entries for the specified account, paginated based on the given limit and offset.
    """
    feeds = collection.find({
        'account_id': str(account_id)
    }).skip(limit * (offset - 1)).limit(limit)

    return __representation(feeds=feeds)
