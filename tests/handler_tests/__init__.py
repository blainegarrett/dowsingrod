import webapp2
import auth_core

from rest_core.utils import get_key_from_resource_id

from tests import BaseCase


class AuthenticatedHandlerTestsBase(BaseCase):
    def setUp(self):
        super(AuthenticatedHandlerTestsBase, self).setUp()

        # Create a User
        user_model = auth_core.create_user('testUser', 'user@test.com', 'Test', 'User')
        login_model = auth_core.create_login(user_model.id, 'basic', 'not_needed_for_basic', 'supersecure')

        # Slightly jank until we make a service for access tokens
        user_entity = get_key_from_resource_id(user_model.id).get()
        login_entity = get_key_from_resource_id(login_model.id).get()

        # Generate the access token and put it on the tests
        self.access_token = auth_core.get_access_token_for_user_and_login(user_entity, login_entity)

    def get_authenticated_request(self, url):
        headers = {'Authorization': 'Bearer ' + self.access_token}
        return webapp2.Request.blank(url, headers=headers)
