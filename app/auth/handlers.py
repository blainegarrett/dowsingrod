import auth_core
from rest_core import handlers
from rest_core.resources import RestField


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
        auth_type = self.cleaned_data['auth_type']
        auth_token = self.cleaned_data['auth_token']

        user, login = auth_core.authenticate(auth_type, auth_token)

        # Step 2: Create a access_token for this user
        access_token = auth_core.get_access_token_for_user_and_login(user, login)

        # TODO: Return basic profile information
        result = {'id_token': 'not_in_use', 'access_token': access_token}
        self.serve_success(result)
        return

