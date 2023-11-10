from django.conf import settings

from feeds.modules.tasks.feeds import update_feeds
from rss_scraper import celery_app


@celery_app.task(name='rss_scraper.update_feeds',
                 queue=settings.QUEUES["UPDATE_FEEDS"])
def update_feeds_task():
    update_feeds()
