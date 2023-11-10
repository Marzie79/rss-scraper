from uuid import uuid4
from typing import List

from bson.objectid import ObjectId

from feeds.modules.decorators.mongo import mongo_connection
from utilities.exceptions import MultiLanguageException
from utilities.messages.error import INVALID_ENTRY_ID


def store_data(collection, feeds: List) -> None:
    """Store feed data in the specified MongoDB collection.

    Args:
        collection: MongoDB collection to store the feed data.
        feeds (list): List of dictionaries representing feed entries.
    """
    collection.insert_many(feeds)


def rss_exist(collection, account_id: uuid4, rss: str) -> bool:
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


def get_all_rss(collection, fields: List):
    """Retrieve aggregated data for distinct values of specified fields.

    Parameters:
        collection: MongoDB collection to query.
        fields (list): List of fields for which to retrieve distinct values.

    Returns:
        Aggregation result containing distinct values for specified fields.
    """
    data = collection.aggregate([{
        '$group': {
            '_id': {
                field: f'${field}'
                for field in fields
            }
        }
    }])

    return data


@mongo_connection
def get_account_feeds(connection, limit: int, offset: int,
                      account_id: uuid4) -> List:
    """Retrieve paginated feed data for a specific account.

    Args:
        connection: MongoDB connection to query.
        limit (int): The number of feed entries to retrieve per page.
        offset (int): The page number to retrieve, with the first page being 1.
        account_id (uuid4): The unique identifier for the associated account.

    Returns:
        A list of feed entries for the specified account, paginated based on the given limit and offset.
    """
    feeds = connection.find({
        'account_id': str(account_id)
    }).skip(limit * (offset - 1)).limit(limit)

    return to_representation(feeds=feeds)


def to_representation(feeds) -> List:
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
