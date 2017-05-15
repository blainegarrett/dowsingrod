"""
Tests For Association Rule Service
"""

from mock import patch
from tests import dataset
from tests import BaseCase
from services import preference_service
from services import rule_service
from models import PreferenceModel


class RulesServiceTestsBase(BaseCase):
    pass


class GenerateAssociationRulesTests(RulesServiceTestsBase):

    def setUp(self):
        super(GenerateAssociationRulesTests, self).setUp()

    def test_base(self):
        u = 0
        models_to_put = []
        for txn in dataset.data2:
            u += 1
            for txn_item in txn:
                models_to_put.append(PreferenceModel("user%s" % u, txn_item, True))
        preference_service.record_preference(models_to_put)

        min_support = .2
        min_confidence = .7

        # Generate Ruleset
        ruleset_model = rule_service.create_ruleset(min_support, min_confidence)

        result = rule_service.generate_association_rules(ruleset_model.id,
                                                         min_support,
                                                         min_confidence)
        self.assertTrue(result)

        # Check generated results
        result = rule_service.query_rules(ruleset_id=ruleset_model.id)

        self.assertEqual(len(result), 31)
        # Check aspects of the result... note: this is ordered by confidence so could be "random"
        #self.assertEqual(result[0].ant, [u'Butter:1', u'Peanut Butter:1'])
        #self.assertEqual(result[0].con,  [u'Bread:1'])
        self.assertEqual(result[0].confidence, 1.0)
        self.assertEqual(result[0].ruleset_id, ruleset_model.id)


@patch('api.mining_api.delete_rules')
class DeleteRulesTests(RulesServiceTestsBase):
    def test_base(self, mock_delete):

        result = rule_service.delete_rules()

        self.assertEqual(result, mock_delete.return_value)
        mock_delete.assert_called_once_with()

'''
@patch('api.mining_api.delete_rules')
class DeleteRulesTests(RulesServiceTestsBase):
    def test_base(self, mock_delete):

        result = rule_service.delete_rules()

        self.assertEqual(result, mock_delete.return_value)
        mock_delete.assert_called_once_with()
'''


@patch('api.mining_api.create_ruleset')
class CreateRulesetTests(RulesServiceTestsBase):
    def test_base(self, mock_create):

        result = rule_service.create_ruleset('arg', kwarg="true")

        self.assertEqual(result, mock_create.return_value)
        mock_create.assert_called_once_with('arg', kwarg='true')
