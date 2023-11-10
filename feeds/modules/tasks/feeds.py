from feeds.modules.decorators.mongo import mongo_connection
from feeds.modules.logics.storages import get_all_rss
from feeds.modules.logics.feeds import fetch_feeds


@mongo_connection
def update_feeds(collection):
    """Update feed data in the MongoDB collection based on account RSS information.

        In this operation the new entities are created, the existing entities are updated
        and the nonexisting entities are deleted.
    
    Args:
        collection: MongoDB collection to update.
    """
    distinct_rss_accounts = get_all_rss(
        collection=collection, fields=['account_id', 'rss', 'feed_modified'])

    for item in distinct_rss_accounts:
        account_id = item['_id']['account_id']
        rss = item['_id']['rss']
        feed_modified = item['_id']['feed_modified']

        feed_data = fetch_feeds(account_id, rss)

        if feed_data and feed_data[0]['feed_modified'] and feed_data[0][
                'feed_modified'] == feed_modified:
            continue

        if feed_data:
            for entry in feed_data:
                collection.update_one(
                    {
                        'id': entry['id'],
                        'account_id': entry['account_id']
                    }, {"$set": entry},
                    upsert=True)
        else:
            collection.delete_many({'rss': rss, 'account_id': rss})

    for item in get_all_rss(collection=collection,
                            fields=['account_id', 'rss', 'feed_modified']):
        if item not in distinct_rss_accounts:
            collection.delete_one({
                'rss': item['_id']['rss'],
                'account_id': item['_id']['account_id'],
                'feed_modified': item['_id']['feed_modified']
            })
