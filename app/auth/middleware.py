import logging
from auth import helpers as auth_helpers
from auth import exceptions as auth_exceptions
from rest_core import errors as rest_exceptions


class AuthenticationMiddleware(object):
    @staticmethod
    def process_request(request):

        try:
            user = auth_helpers.get_user_from_request(request)
            setattr(request, '_user', user)
        except auth_exceptions.AuthenticationError, e:
            logging.error(e)
            raise rest_exceptions.AuthenticationException("Authentication Failed")
