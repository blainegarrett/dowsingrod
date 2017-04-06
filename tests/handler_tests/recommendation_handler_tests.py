import webapp2
import json
import main
from tests import BaseCase
from tests import dataset
from models import PreferenceModel
from services import preference_service


class RecommendationHandlerTestsBase(BaseCase):
    pass


class RuleSetCollectionHandlerTests(RecommendationHandlerTestsBase):
    def test_empty_get(self):

        request = webapp2.Request.blank('/api/rest/v1.0/rulesets?verbose=true')
        #   Get a response for that request.
        response = request.get_response(main.app)

        # Let's check if the response is correct.
        self.assertEqual(response.status_int, 200)

    def test_post(self):
        # Generate Ruleset
        request = webapp2.Request.blank('/api/rest/v1.0/rulesets?verbose=true')
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
        url = '/api/rest/v1.0/rulesets?min_confidence=.345&min_support=.45&verbose=true'
        request = webapp2.Request.blank(url)
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


class AssociationRulesCollectionHandlerTests(RecommendationHandlerTestsBase):

    def setUp(self):
        super(AssociationRulesCollectionHandlerTests, self).setUp()

        u = 0
        models_to_put = []
        for txn in dataset.data2:
            u += 1
            for txn_item in txn:
                models_to_put.append(PreferenceModel("user%s" % u, txn_item, True))
        preference_service.record_preference(models_to_put)

        # Generate 2 association rule sets on the same data with different confidence
        url = '/api/rest/v1.0/rulesets?min_confidence=.1&min_support=.1&verbose=true'
        request = webapp2.Request.blank(url)
        request.method = 'POST'
        request.content_type = 'application/json'
        response = request.get_response(main.app)
        self.assertEqual(response.status_int, 200)
        result = json.loads(response.body)

        self.ruleset_id1 = result['results']['resource_id']

        url = '/api/rest/v1.0/rulesets?min_confidence=.70&min_support=.45&verbose=true'
        request = webapp2.Request.blank(url)
        request.method = 'POST'
        request.content_type = 'application/json'
        response = request.get_response(main.app)
        self.assertEqual(response.status_int, 200)
        result = json.loads(response.body)

        self.ruleset_id2 = result['results']['resource_id']

    def test_get(self):
        # Get w/o rule param
        request = webapp2.Request.blank('/api/rest/v1.0/recommendations?verbose=true')
        request.method = 'GET'
        request.content_type = 'application/json'
        response = request.get_response(main.app)

        # Let's check if the response is correct.
        self.assertEqual(response.status_int, 200)
        result = json.loads(response.body)
        self.assertEquals(12, len(result['results']))

        # Re-run with a specific ruleset id
        url = '/api/rest/v1.0/recommendations?verbose=true&ruleset_id=' + self.ruleset_id1
        request = webapp2.Request.blank(url)
        request.method = 'GET'
        request.content_type = 'application/json'

        #  Get a response for that request.
        response = request.get_response(main.app)

        # Let's check if the response is correct.
        self.assertEqual(response.status_int, 200)
        result = json.loads(response.body)
        self.assertEquals(78, len(result['results']))
