import json
import main

from tests.handler_tests import AuthenticatedHandlerTestsBase
from models import PreferenceModel
from services import preference_service


class PreferenceHandlerTestsBase(AuthenticatedHandlerTestsBase):
    pass


class PreferenceCollectionHandlerTests(PreferenceHandlerTestsBase):
    def test_empty_get(self):

        request = self.get_authenticated_request('/api/rest/v1.0/preferences?verbose=true')
        #   Get a response for that request.
        response = request.get_response(main.app)

        # Let's check if the response is correct.
        self.assertEqual(response.status_int, 200)

    def test_post(self):
        request = self.get_authenticated_request('/api/rest/v1.0/preferences?verbose=true')
        request.method = 'POST'
        request.content_type = 'application/json'
        request.body = json.dumps([{'item_id': 'asdf', 'pref': True, 'user_id': 'user1'}])
        #   Get a response for that request.
        response = request.get_response(main.app)

        # Let's check if the response is correct.
        self.assertEqual(response.status_int, 200)


class PreferenceDetailHandlerTests(PreferenceHandlerTestsBase):
    """
    """
    def test_get_404(self):

        request = self.get_authenticated_request('/api/rest/v1.0/preferences/asdf?verbose=true')
        #   Get a response for that request.
        response = request.get_response(main.app)

        # Let's check if the response is correct.
        self.assertEqual(response.status_int, 404)
        self.assertTrue("Preference with resource_id \'asdf\' not found" in response.body)

    def test_get_success(self):
        p = PreferenceModel('u1', 'i1', True, None)
        p = preference_service.record_preference(p)

        request = self.get_authenticated_request('/api/rest/v1.0/preferences/%s?verbose=true' % p.id)
        #   Get a response for that request.
        response = request.get_response(main.app)

        # Let's check if the response is correct.
        self.assertEqual(response.status_int, 200)
        self.assertTrue(p.id in response.body)
