"""
Auth System Helpers
"""
import datetime
import logging
import jwt

from rest_core.utils import get_key_from_resource_id, get_resource_id_from_key  # TODO: Don't depend on REST
from auth.exceptions import AuthenticationError
from auth.entities import AnonymousAuthUser, AuthUser, AuthUserMethod, AuthLogin
from auth.constants import REQUEST_USER_KEY
from auth.services import basic

from auth_settings import JWT_SECRET, JWT_ISSUER, JWT_AUDIENCE


JWT_ALGORITHM = 'HS256'
JWT_EXPIRATION = 60 * 60 # 1 hour


def mark_user_authenticated(user, login):
    """
    Modify a User so it knows it is logged in - checked via user.is_authenticated()
    """
    setattr(user, '_active_login', login)
    return user

def get_user_by_auth_attempt(auth_scheme, auth_credentials):
    """
    Given a auth_type and auth_token, attempt to authenticate
    """
    if (auth_scheme.lower() == 'basic'):
        # Using Basic Auth - dip into service
        return basic.get_user_by_token(auth_credentials)
    elif (auth_scheme.lower() == 'bearer'):
        # This is our internal access token
        return get_user_from_access_token(auth_credentials)
    else:
        raise AuthenticationError("Unsupported authentication type: %s" % auth_scheme)


def get_user_from_request(request):
    """
    Given a request, attempt to authenticate based on Auth Header Scheme/Credentials
    Called via the middleware, etc
    """

    # Step 1: Detect if we have an Auth Header
    raw_auth_header_val = request.headers.get('Authorization', None)
    if not raw_auth_header_val:
        return AnonymousAuthUser()

    # Step 2: Detect the Authorization type
    auth_scheme, auth_credentials = get_auth_type_and_token_from_header(raw_auth_header_val)

    # Step 3: Based on type, proceed
    user, login = get_user_by_auth_attempt(auth_scheme, auth_credentials)

    # Step 4: Activate
    return mark_user_authenticated(user, login)


def get_auth_type_and_token_from_header(raw_auth_header_val):
    """
    Return an Auth Header's Type and Token
    Input should be in the form of 'Barer token data' or 'Basic token data'
    """
    if not raw_auth_header_val:
        raise AuthenticationError("No Header Value Given")
    return raw_auth_header_val.split(' ', 1)


def get_access_token_payload_for_user(user, login):
    """
    Put together a payload for the user
    """
    payload = {
        'username': user.username,
        # 'is_authenticated': user.is_authenticated(),
        'id': None,
        'login_auth_type': None
    }

    if isinstance(user, AuthUser):
        payload['id'] = get_resource_id_from_key(user.key) # TODO: Switch to id
        payload['login_auth_type'] = login.auth_type # Which service they used to login

    return payload


def make_access_token(user_payload):
    now = datetime.datetime.utcnow()
    jwt_payload = {
        'exp': now + datetime.timedelta(seconds=JWT_EXPIRATION),
        'aud': JWT_AUDIENCE,
        'iss': JWT_ISSUER,
        'iat': now,
        'data': user_payload
    }

    token = jwt.encode(jwt_payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token


def read_access_token(access_token):
    # Decode the payload
    try:
        return jwt.decode(access_token, JWT_SECRET, algorithm=JWT_ALGORITHM,
                          audience=JWT_AUDIENCE, issuer=JWT_ISSUER)

    except jwt.ExpiredSignatureError, e:
        # Token has expired
        logging.error("JWT Expired: " + str(e))
        raise AuthenticationError("JWT Token Expired")

    except jwt.InvalidTokenError, e:
        # Log the JWT exception for debugging
        logging.error("JWT Decode Error" + str(e))
        raise AuthenticationError("Unable to decode JWT token")


def get_user_from_access_token(access_token):
    """
    Decode Access token and return a corresponding user
    """
    payload = read_access_token(access_token)

    # Resolve the user
    user_data = payload.get('data', None)
    if not (user_data):
        raise Exception('Unable to get data off valid token. Version error?')

    user_resource_id = user_data.get('id', None)
    user_key = get_key_from_resource_id(user_resource_id)
    user = user_key.get()

    # Get the active login used originally. Note: We don't validate here - pw, etc...
    login_auth_type = user_data.get('login_auth_type', None)
    if not login_auth_type:
        # How did you originally login?
        raise Exception("Could not determine login auth type from key")

    l_key = AuthLogin.generate_key(user.key, login_auth_type) # TODO: This should be encoded into the jwt_token
    login = l_key.get()

    return user, login