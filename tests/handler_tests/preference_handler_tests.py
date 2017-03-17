import webapp2
import json
import main
from tests import BaseCase
from models import PreferenceModel
from services import preference_service


class PreferenceHandlerTestsBase(BaseCase):
    pass


class PreferenceCollectionHandlerTests(PreferenceHandlerTestsBase):
    def test_empty_get(self):

        request = webapp2.Request.blank('/api/rest/v1.0/preferences')
        #   Get a response for that request.
        response = request.get_response(main.app)

        # Let's check if the response is correct.
        self.assertEqual(response.status_int, 200)

    def test_post(self):
        request = webapp2.Request.blank('/api/rest/v1.0/preferences')
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

        request = webapp2.Request.blank('/api/rest/v1.0/preferences/asdf')
        #   Get a response for that request.
        response = request.get_response(main.app)

        # Let's check if the response is correct.
        self.assertEqual(response.status_int, 404)
        self.assertTrue("Preference with resource_id \'asdf\' not found" in response.body)

    def test_get_success(self):
        p = PreferenceModel('u1', 'i1', True, None)
        p = preference_service.record_preference(p)

        request = webapp2.Request.blank('/api/rest/v1.0/preferences/%s' % p.id)
        #   Get a response for that request.
        response = request.get_response(main.app)

        # Let's check if the response is correct.
        self.assertEqual(response.status_int, 200)
        self.assertTrue(p.id in response.body)
