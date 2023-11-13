from typing import List
from uuid import uuid4

import feedparser

from feeds.modules.decorators.utils import retry_failure


@retry_failure()
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
    entries_details = {'rss': rss, 'account_id': str(account_id)}

    for key in list(feeds.feed.keys()):
        entries_details[f'parent_{key}'] = feeds.feed[key]

    for entry in entries:
        entry_detail = entries_details.copy()

        for key in entry.keys():
            entry_detail[key] = entry[key]

        result.append(entry_detail)

    return result
