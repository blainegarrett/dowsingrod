from rest_core import handlers
from rest_core.resources import Resource
from rest_core.resources import RestField

from auth import helpers

class BaseAuthHandler(handlers.RestHandlerBase):
    """
    Base Handler for Auth Services
    """
    def get_param_schema(self):
        return {}

# Fields for Authentication
AUTH_FIELDS = [
    RestField('auth_type', required=True),
    RestField('auth_token', required=True),
]

class AuthenticationHandler(BaseAuthHandler):
    """
    Handler to authenticate (password, etc)
    Accessible via: /api/auth/authenticate (see main.py)
    """

    def get_rules(self):
        return AUTH_FIELDS

    def post(self):
        """
        Attempt to authenticate with auth_type and auth_token data
        eg. {'auth_type':'Basic', auth_token: base64.encode('username:password')}
        """

        # Step 1: Authenticate the user get the associated login. Throws AuthenticationException
        user, login = helpers.get_user_by_auth_attempt(self.cleaned_data['auth_type'],
                                                       self.cleaned_data['auth_token'])

        # Step 2: Create a access_token for this user
        user_payload = helpers.get_access_token_payload_for_user(user, login)
        access_token = helpers.make_access_token(user_payload) # returns a jwt token

        # TODO: Return basic profile information
        result = {'id_token': 'not_in_use', 'access_token': access_token}
        self.serve_success(result)
        return

