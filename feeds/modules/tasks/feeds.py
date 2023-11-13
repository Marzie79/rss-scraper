from typing import List

from feeds.modules.decorators.mongo import mongo_connection
from feeds.modules.logics.feeds import fetch_feeds


def __get_all_rss(collection, fields: List):
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
def update_feeds(collection):
    """Update feed data in the MongoDB collection based on account RSS information.

        In this operation the new entities are created, the existing entities are updated
        and the nonexisting entities are deleted.
    
    Args:
        collection: MongoDB collection to update.
    """
    distinct_rss_accounts = __get_all_rss(
        collection=collection, fields=['account_id', 'rss', 'parent_updated'])

    for item in distinct_rss_accounts:
        account_id = item['_id']['account_id']
        rss = item['_id']['rss']
        parent_updated = item['_id']['parent_updated']

        feed_data = fetch_feeds(account_id, rss)

        if feed_data and feed_data[0]['parent_updated'] and feed_data[0][
                'parent_updated'] == parent_updated:
            continue

        if feed_data:
            for entry in feed_data:
                collection.update_one(
                    {
                        'id': entry['id'],
                        'account_id': entry['account_id']
                    }, {'$set': entry},
                    upsert=True)
        else:
            collection.delete_many({'rss': rss, 'account_id': rss})

    for item in __get_all_rss(collection=collection,
                              fields=['account_id', 'rss', 'parent_updated']):
        if item not in distinct_rss_accounts:
            collection.delete_one({
                'rss': item['_id']['rss'],
                'account_id': item['_id']['account_id'],
                'parent_updated': item['_id']['parent_updated']
            })
