import os

from django.conf import settings
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rss_scraper.settings.base')

app = Celery('rss_scraper')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
app.conf.task_default_routing_key = settings.RSS_SCRAPER_RABBIT_INFORMATION['EXCHANGE']
app.conf.task_default_exchange = settings.RSS_SCRAPER_RABBIT_INFORMATION['ROUTING_KEY']
app.conf.task_queues = []
