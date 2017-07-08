import logging
from auth_core import get_user_from_request
from auth_core import AuthenticationException


class AuthenticationMiddleware(object):
    @staticmethod
    def process_request(request):

        try:
            user = get_user_from_request(request)
            setattr(request, '_user', user)
        except AuthenticationException, e:
            logging.error(e)
            raise AuthenticationException("Authentication Failed")
