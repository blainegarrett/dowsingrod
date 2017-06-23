"""
Auth System Helpers
"""

from auth.exceptions import AuthenticationError
from auth.entities import AnonymousAuthUser, AuthUser, AuthUserMethod, AuthLogin
from auth.constants import REQUEST_USER_KEY
from auth.services import basic


def mark_user_authenticated(user, login):
    """
    Modify a User so it knows it is logged in - checked via user.is_authenticated()
    """
    setattr(user, '_active_login', login)
    return user


def get_user_from_request(request):
    """
    Given a request, attempt to authenticate and return a User or AnonymousAuthUser

    TODO: Wrap this in a bunch of try catch
    TODO: If header is over x minutes old, requery the datastore to update
    TODO: Needs Unit Tests
    """

    # Step 1: Detect if we have an Auth Header
    raw_auth_header_val = request.headers.get('Authorization', None)
    if not raw_auth_header_val:
        return AnonymousAuthUser()

    # Step 2: Detect the Authorization type
    authorization_type, authorization_token = get_auth_type_and_token_from_header(raw_auth_header_val)

    # Step 3: Based on type, proceed
    # TODO: Library this a bit more?
    if (authorization_type == 'Basic'):
        user, login = basic.get_user_by_token(authorization_token)

        # TODO: Set the active login on the user
        return mark_user_authenticated(user, login)
        # TODO: If this is a "login attempt", audit the successful login

        # NEXT UP: MAKE A BASIC AUTHENTICATION LIB
        # user = lib.get_user(authorization_token)
        # return user

    else:
        raise AuthenticationError("Unsupported authentication type: %s" % authorization_type)


def get_auth_type_and_token_from_header(raw_auth_header_val):
    """
    Return an Auth Header's Type and Token
    Input should be in the form of 'Barer token data' or 'Basic token data'
    """
    if not raw_auth_header_val:
        raise AuthenticationError("No Header Value Given")
    return raw_auth_header_val.split(' ', 1)
