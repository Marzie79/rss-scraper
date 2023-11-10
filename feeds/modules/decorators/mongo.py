from functools import wraps

from django.conf import settings
from pymongo import MongoClient


def mongo_connection(func):
    """Decorator for establishing a MongoDB connection.
    
        Executing the wrapped function with a MongoDB collection,
        and ensuring proper connection closure.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            client = MongoClient(
                f'{settings.MONGO_HOST}:{settings.MONGO_PORT}',
                username=settings.MONGO_USERNAME,
                password=settings.MONGO_PASSWORD)

            db = client[settings.MONGO_DATABASE]
            collection = db[settings.MONGO_COLLECTION]

            result = func(collection, *args, **kwargs)

        finally:
            client.close()

        return result

    return wrapper
