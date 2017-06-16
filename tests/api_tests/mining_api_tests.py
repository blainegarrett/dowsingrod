# from mock import patch
import datetime
from mock import patch
from tests import BaseCase
from api import mining_api

BDAY_TUPLE = (1982, 9, 2, 16, 30, 0)  # yay my birthday


class MiningTestsBase(BaseCase):
    pass


# Association RuleSet Tests
'''
class QueryRuleSetEntitiesTests(MiningTestsBase):
    """
    Tests around querying for Association RulesSets
    """
    def setUp(self):
        super(QueryRuleSetEntitiesTests, self).setUp()

        m2 = mining_api.AssociationRuleModel(['Cheese:1', 'Peanut Butter:0'],
                                             ['Steak:1'],
                                             .25)

        mining_api.create_rules('ruleset_id', [m1, m2])

    def test_no_params(self):
        raise Exception('not yet')
        result = mining_api._query_rule_entities()

        self.assertEqual(len(result), 2)
        self.assertTrue(isinstance(result[0], mining_api.AssociationRuleEntity))
        self.assertTrue(isinstance(result[1], mining_api.AssociationRuleEntity))
'''


class CreateRulesetTests(MiningTestsBase):

    @patch('api.mining_api.get_resource_id_from_key', return_value='mocked_id')
    def test_base(self, m_get_id):
        result = mining_api.create_ruleset(.4, .7)

        self.assertTrue(isinstance(result, mining_api.AssociationRuleSetModel))
        self.assertEqual(result.min_confidence, .7)
        self.assertEqual(result.min_support, .4)
        self.assertEqual(result.total_rules, None)
        self.assertTrue(isinstance(result.created_timestamp, datetime.datetime))
        self.assertEqual(result.id, 'mocked_id')

# Association Rule Tests


class RuleModelTests(MiningTestsBase):
    def test_get_rule_item_id(self):
        """
        Ensure we can generate a composite pref id for use in txn lists
        representing item and if the session user liked it or not.
        """

        rule_model = mining_api.AssociationRuleModel(['Peanut Butter:1', 'Steak:0', 'Peanut Butter:0'],
                                                     ['Cheese:0'],
                                                     .25)

        self.assertEqual(rule_model.generate_rule_key(), 'peanut_butter:0__peanut_butter:1__steak:0')


class QueryRuleEntitiesTests(MiningTestsBase):
    """
    Tests around querying for Association Rules
    """
    def setUp(self):
        super(QueryRuleEntitiesTests, self).setUp()

        m1 = mining_api.AssociationRuleModel(['Peanut Butter:1', 'Steak:0', 'Peanut Butter:0'],
                                             ['Cheese:0'],
                                             .25)
        m2 = mining_api.AssociationRuleModel(['Cheese:1', 'Peanut Butter:0'],
                                             ['Steak:1'],
                                             .25)

        mining_api.create_rules('ruleset_id', [m1, m2])

    def test_no_params(self):
        result, cursor, more = mining_api._query_rule_entities()

        self.assertEqual(len(result), 2)
        self.assertTrue(isinstance(result[0], mining_api.AssociationRuleEntity))
        self.assertTrue(isinstance(result[1], mining_api.AssociationRuleEntity))


class QueryRuleModelsTests(MiningTestsBase):
    @patch('api.mining_api._query_rule_entities')
    @patch('api.mining_api._populate_rule_model')
    def test_base(self, mock_populate, mock_query):
        # Setup Mocks
        mock_query.return_value = (['a', 'b'], None, False)

        # Run Code To Test
        result = mining_api.query_rule_models(limit=4, kwarg=True)

        # Check results
        self.assertEqual(result, ([mock_populate.return_value, mock_populate.return_value], None, False))
        mock_query.assert_called_once_with(limit=4, kwarg=True)


@patch('api.mining_api.get_resource_id_from_key', return_value='mocked_id')
class CreateRuleTest(MiningTestsBase):
    """Tests around creating a single AssociationRuleModel"""

    def test_base(self, m_get_id):
        ant = ['Peanut Butter:1', 'Steak:0', 'Peanut Butter:0']
        con = ['Cheese:0']

        m = mining_api.AssociationRuleModel(ant, con, .85)
        result = mining_api.create_rule('ruleset_id', m)

        self.assertTrue(isinstance(result, mining_api.AssociationRuleModel))
        self.assertEqual(result.ant, ['Peanut Butter:1', 'Steak:0', 'Peanut Butter:0'])
        self.assertEqual(result.con, ['Cheese:0'])
        self.assertEqual(result.confidence, .85)
        self.assertEqual(result.rule_key, 'peanut_butter:0__peanut_butter:1__steak:0')
        self.assertEqual(result.id, 'mocked_id')
        self.assertEqual(result.ruleset_id, 'ruleset_id')


@patch('api.mining_api.get_resource_id_from_key', return_value='mocked_id')
class CreateMultiTest(MiningTestsBase):
    """Tests around creating multiple AssociationRuleModel at once"""
    def test_base(self, m_get_id):
        ant = ['Peanut Butter:1', 'Steak:0', 'Peanut Butter:0']
        con = ['Cheese:0']

        m1 = mining_api.AssociationRuleModel(ant, con, .85)
        m2 = mining_api.AssociationRuleModel(ant, con, .85)
        result = mining_api.create_rules('ruleset_id', [m1, m2])

        self.assertTrue(isinstance(result, list))

        self.assertTrue(isinstance(result[0], mining_api.AssociationRuleModel))
        self.assertEqual(result[0].ant, ant)
        self.assertEqual(result[0].con, con)
        self.assertEqual(result[0].confidence, .85)
        self.assertEqual(result[0].rule_key, 'peanut_butter:0__peanut_butter:1__steak:0')
        self.assertEquals(result[0].id, 'mocked_id')
        self.assertEqual(result[0].ruleset_id, 'ruleset_id')

        self.assertEqual(m_get_id.call_count, 2)


class DeleteRulesTests(MiningTestsBase):
    def setUp(self):
        super(DeleteRulesTests, self).setUp()

        m1 = mining_api.AssociationRuleModel(['Peanut Butter:1', 'Steak:0', 'Peanut Butter:0'],
                                             ['Cheese:0'],
                                             .25)
        mining_api.create_rules('ruleset_id', [m1])

    def base_test(self):

        self.assertEqual(1, len(mining_api.query_rule_models()[0]))
        mining_api.delete_rules()
        self.assertEqual(0, len(mining_api.query_rule_models()[0]))

"""

class DeleteRulesSinceTests(MiningTestsBase):
    def base_test(self):
        result = mining_api.delete_rules_since()
"""


"""

class RunAprioriTests(MiningTestsBase):
    def base_test(self):
        result = mining_api.run_apriori()
"""
"""

class PrintItemsAndRulesTests(MiningTestsBase):
    def base_test(self):
        result = mining_api._print_items_and_rules()

"""
"""

class PopulateEntityTests(MiningTestsBase):
    def base_test(self):
        result = mining_api._populate_entity()
"""
