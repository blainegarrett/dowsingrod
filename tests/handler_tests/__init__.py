import webapp2
import auth_core

from tests import BaseCase


class AuthenticatedHandlerTestsBase(BaseCase):
    def setUp(self):
        super(AuthenticatedHandlerTestsBase, self).setUp()

        # Create a User
        user = auth_core.create_user('testUser', 'user@test.com', 'Test', 'User')
        login = auth_core.create_login(user, 'basic', 'not_needed_for_basic', 'supersecure')
        self.access_token = auth_core.get_access_token_for_user_and_login(user, login)

    def get_authenticated_request(self, url):
        headers = {'Authorization': 'Bearer ' + self.access_token}
        return webapp2.Request.blank(url, headers=headers)
