import os

import jwt
from rest_framework.response import Response
from jwt.exceptions import DecodeError

from codefuture_bank.settings import SECRET_KEY


def authorization(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            decoded_token = jwt.decode(request.META.get("HTTP_AUTHORIZATION"), SECRET_KEY, algorithms=['HS256'])
            return func(self, request, decoded_token)
        except DecodeError:
            return Response({"message": "token is invalid"})

    return wrapper
