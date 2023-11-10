from django.conf import settings

from utilities.exceptions import MultiLanguageException
from utilities.messages.error import SERVER_ERROR


def retry_failure(repetition: int = settings.RETRY_FAILURE):
    """Retry a process for a specific time.
    
    Args:
        repetition(int): The time that we want to repeat a process.
    """

    def decorator_retry(func):

        def wrapper(*args, **kwargs):
            for counter in range(repetition):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    if counter == repetition - 1:
                        raise MultiLanguageException(SERVER_ERROR)
            return

        return wrapper

    return decorator_retry
