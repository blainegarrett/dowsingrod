import auth_core
import voluptuous
from auth_core.decorators import authentication_required
from auth_core.services import users_service
from rest_core import handlers
from rest_core.resources import RestField
from rest_core.resources import ResourceIdField
from rest_core.resources import Resource
from rest_core.exc import DoesNotExistException

# Fields for Authentication
AUTH_FIELDS = [
    RestField('auth_type', required=True),
    RestField('auth_token', required=True),
]


AUTH_USER_REST_RULES = [
    ResourceIdField(output_only=True),
    RestField(auth_core.AuthUser.first_name, required=True),
    RestField(auth_core.AuthUser.last_name, required=True),
    RestField(auth_core.AuthUser.username, required=False),
    RestField(auth_core.AuthUser.email, required=False),
    RestField(auth_core.AuthUser.is_activated, required=False),
]


class AuthenticationHandler(handlers.RestHandlerBase):
    """
    Handler to authenticate (password, etc)
    Accessible via: /api/auth/authenticate (see main.py)
    """

    def get_rules(self):
        return AUTH_FIELDS

    def post(self):
        """
        Attempt to authenticate with auth_type and auth_token data
        eg. payload = {'auth_type':'Basic', auth_token: base64.encode('username:password')}
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


class UsersCollectionHandler(handlers.RestHandlerBase):
    """
    Users Collection REST Endpoint
    Accessible via: /api/auth/users (see main.py)
    """
    def get_param_schema(self):
        return {
            'limit': voluptuous.Coerce(int),
            'cursor': voluptuous.Coerce(str),
        }

    def get_rules(self):
        return AUTH_USER_REST_RULES

    @authentication_required
    def get(self):

        cursor = self.cleaned_params.get('cursor')
        limit = self.cleaned_params.get('limit')

        entities, next_cursor, more = users_service.get_auth_users(limit=limit, cursor=cursor)

        # Create A set of results based upon this result set - iterator??
        return_resources = []
        for e in entities:
            return_resources.append(Resource(e, AUTH_USER_REST_RULES).to_dict())
        self.serve_success(return_resources, {'cursor': next_cursor, 'more': more})

    @authentication_required
    def post(self):
        """
        Create a User
        Note: This does not create a Login ... yet?
        """
        e = users_service.create_auth_user(self.cleaned_data)
        self.serve_success(Resource(e, AUTH_USER_REST_RULES).to_dict())


class UserResourceHandler(handlers.RestHandlerBase):
    """
    User Resource REST Endpoint
    Accessible via: /api/auth/users/<resource_id> (see main.py)
    """

    def get_rules(self):
        return AUTH_USER_REST_RULES

    @authentication_required
    def get(self, user_resource_id):
        """
        Return an authuser resource given by user_resource_id
        """

        user = self._get_model_by_id_or_error(user_resource_id)

        # Convert to Rest Resource
        self.serve_success(Resource(user, AUTH_USER_REST_RULES).to_dict())

    @authentication_required
    def put(self, user_resource_id):
        """
        Update and return authuser resource.
        Note: This does not update the Login, yet...
        """

        user = self._get_model_by_id_or_error(user_resource_id)
        user = users_service.update_user(user, self.cleaned_data)

        # Convert to Rest Resource
        self.serve_success(Resource(user, AUTH_USER_REST_RULES).to_dict())

    def _get_model_by_id_or_error(self, user_resource_id):
        """
        Resolve an auth_user by id or throw a 404
        """

        user = users_service.get_by_id(user_resource_id)
        if not user:
            raise DoesNotExistException("Could not find user with id %s" % user_resource_id)
        return user
