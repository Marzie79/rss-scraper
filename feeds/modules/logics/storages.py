from uuid import uuid4
from typing import List

from bson.objectid import ObjectId

from feeds.modules.decorators.mongo import mongo_connection


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
def book_mark(collection, id: str, bookmark: bool = True) -> None:
    """Update the bookmark status for a specific entry in the MongoDB collection.

    Args:
        collection: MongoDB collection to update.
        id (str): The ObjectId of the entry to be updated.
        bookmark (bool): The bookmark status to set.
    """
    collection.update_one({"_id": ObjectId(id)},
                          {'$set': {
                              'book_mark': bookmark
                          }})


def get_all_rss(collection, fields: List):
    """Retrieve aggregated data for distinct values of specified fields.

    Parameters:
        collection: MongoDB collection to query.
        fields (list): List of fields for which to retrieve distinct values.

    Returns:
        Aggregation result containing distinct values for specified fields.
    """
    data = collection.aggregate([{
        "$group": {
            "_id": {
                field: f'${field}'
                for field in fields
            }
        }
    }])

    return data
