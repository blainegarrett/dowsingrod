import webapp2
import json
import main
from tests import BaseCase


class RecommendationHandlerTestsBase(BaseCase):
    pass


class RuleSetCollectionHandlerTests(RecommendationHandlerTestsBase):
    def test_empty_get(self):

        request = webapp2.Request.blank('/api/rest/v1.0/rulesets')
        #   Get a response for that request.
        response = request.get_response(main.app)

        # Let's check if the response is correct.
        self.assertEqual(response.status_int, 200)

    def test_post(self):
        # Generate Ruleset
        request = webapp2.Request.blank('/api/rest/v1.0/rulesets')
        request.method = 'POST'
        request.content_type = 'application/json'

        #   Get a response for that request.
        response = request.get_response(main.app)

        # Let's check if the response is correct.
        self.assertEqual(response.status_int, 200)
        result = json.loads(response.body)

        self.assertEqual(result['results']['min_confidence'], .5)  # Default
        self.assertEqual(result['results']['min_support'], .75)  # Default

    def test_post_with_params(self):
        # Generate Ruleset with min requirements
        request = webapp2.Request.blank('/api/rest/v1.0/rulesets?min_confidence=.345&min_support=.45')
        request.method = 'POST'
        request.content_type = 'application/json'

        #   Get a response for that request.
        response = request.get_response(main.app)

        # Let's check if the response is correct.
        self.assertEqual(response.status_int, 200)
        result = json.loads(response.body)

        self.assertEqual(result['results']['_meta']['resource_type'], 'AssociationRuleSetModel')

        self.assertEqual(result['results']['min_confidence'], 0.345)
        self.assertEqual(result['results']['min_support'], .45)



'''
class RecommendatioDetailHandlerTests(RecommendationHandlerTestsBase):
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
'''
