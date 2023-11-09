from rest_framework.exceptions import APIException
from rest_framework import status


class MultiLanguageException(APIException):
    status_code = status.HTTP_417_EXPECTATION_FAILED

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.detail:
            self.detail = {'errors': self.detail}
