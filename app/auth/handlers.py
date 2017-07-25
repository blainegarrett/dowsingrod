import auth_core
import voluptuous
from auth_core.decorators import authentication_required
from auth_core.services import users_service
from auth_core.services import logins_service
from auth_core import DuplicateCredentials

from rest_core import handlers
from rest_core.resources import RestField
from rest_core.resources import ResourceIdField
from rest_core.resources import Resource
from rest_core.exc import DoesNotExistException
from rest_core.exc import BadRequestException


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

AUTH_METHOD_REST_RULES = [
    ResourceIdField(output_only=True),
    RestField(auth_core.AuthUserMethod.auth_type, required=True),
    RestField(auth_core.AuthUserMethod.auth_key, required=True),
    RestField(auth_core.AuthUserMethod.auth_data, required=False),
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
        """
        Fetch a paginated list of users
        """
        cursor = self.cleaned_params.get('cursor')
        limit = self.cleaned_params.get('limit')

        user_models, next_cursor, more = users_service.get_auth_users(limit=limit, cursor=cursor)

        # Create A set of results based upon this result set
        return_resources = []
        for user_model in user_models:
            return_resources.append(Resource(user_model, AUTH_USER_REST_RULES).to_dict())
        self.serve_success(return_resources, {'cursor': next_cursor, 'more': more})

    @authentication_required
    def post(self):
        """
        Create a User
        Note: This does not create a login for the user
        """

        user_model = users_service.create_auth_user(self.cleaned_data)
        self.serve_success(Resource(user_model, AUTH_USER_REST_RULES).to_dict())


class UserBaseHandler(handlers.RestHandlerBase):
    def get_user_or_404(self, user_resource_id):
        """
        Helper to resolve a user or throw a 404
        """

        user_model = users_service.get_by_id(user_resource_id)
        if not user_model:
            raise DoesNotExistException("Could not find user with id %s" % user_resource_id)
        return user_model


class UserResourceHandler(UserBaseHandler):
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

        user_model = self.get_user_or_404(user_resource_id)

        # Convert to Rest Resource
        self.serve_success(Resource(user_model, AUTH_USER_REST_RULES).to_dict())

    @authentication_required
    def put(self, user_resource_id):
        """
        Update and return authuser resource.
        Note: This does not update the Login, yet...
        """

        user_model = self.get_user_or_404(user_resource_id)

        user_model = users_service.update_user(user_model, self.cleaned_data)

        # Convert to Rest Resource
        self.serve_success(Resource(user_model, AUTH_USER_REST_RULES).to_dict())


class UserLoginsBaseHandler(UserBaseHandler):

    def create_sanitized_resource(self, login_model):
        """
        Given a login model, convert to REST resource and clean up sensitive fields
        """

        resource = Resource(login_model, AUTH_METHOD_REST_RULES).to_dict()

        # TODO: Maybe just delete the key?
        resource['auth_data'] = '--redacted--'
        return resource


class UserLoginsCollectionHandler(UserLoginsBaseHandler):
    """
    Handler for accessing a user'a login
    Accessible via: /api/auth/users/<user_resource_id>/logins (see main.py)
    """
    def get_rules(self):
        return AUTH_METHOD_REST_RULES

    @authentication_required
    def post(self, user_resource_id):
        """
        Create a new Login for a given user
        Note: If there is already a login for the combo of user, type, auth_key this will error
        """

        # Ensure User exists
        user_model = self.get_user_or_404(user_resource_id)

        # TODO: Catch all the potential errors - duplicate == badrequest'
        try:
            login_model = logins_service.create_login(user_model.id, self.cleaned_data)
        except DuplicateCredentials, e:
            raise BadRequestException(e)

        # Serve up results
        self.serve_success(self.create_sanitized_resource(login_model))

    @authentication_required
    def get(self, user_resource_id):
        """
        Fetch all logins for a given
        """

        # Ensure User exists
        user_model = self.get_user_or_404(user_resource_id)

        # Fetch all logins for this user
        login_models = logins_service.get_logins_for_user(user_model.id)

        # Serve up Results
        return_resources = []
        for login_model in login_models:
            return_resources.append(self.create_sanitized_resource(login_model))

        self.serve_success(return_resources)


class UserLoginsResourceHandler(UserLoginsBaseHandler):
    """
    Handler for accessing a specific user login
    Accessible via: /api/auth/users/<user_resource_id>/logins/<login_resource_id> (see main.py)
    """

    def get_rules(self):
        return AUTH_METHOD_REST_RULES

    @authentication_required
    def get(self, user_resource_id, login_resource_id):
        """
        Fetch a specific login for a given user
        """

        # Ensure User exists
        user_model = self.get_user_or_404(user_resource_id)

        # Get the target login model
        login_model = logins_service.get_login_by_id(login_resource_id)
        if not login_model:
            raise DoesNotExistException("Login does not exist.")

        # Ensure the login belongs to the user
        if not login_model.user_resource_id == user_model.id:
            raise BadRequestException("Login does not belong to this user.")

        # Serve up results
        self.serve_success(self.create_sanitized_resource(login_model))

    @authentication_required
    def put(self, user_resource_id, login_resource_id):
        """
        Update a login for a given user
        Note: This is used to change password, etc
            - the auth_data field should be the raw password on the incomming request
        """
        # Note: auth_type, auth_key, etc are ignored on update TODO: Don't make required

        # Ensure User exists
        user_model = self.get_user_or_404(user_resource_id)

        # Get the target login model
        login_model = logins_service.get_login_by_id(login_resource_id)
        if not login_model:
            raise DoesNotExistException("Login does not exist.")

        # Ensure the login belongs to the user
        if not login_model.user_resource_id == user_model.id:
            raise BadRequestException("Login does not belong to this user.")

        # Update it
        try:
            login_model = logins_service.update_login(login_model, self.cleaned_data)
        except ValueError, e:
            raise BadRequestException(e)

        # Serve up results
        self.serve_success(self.create_sanitized_resource(login_model))
