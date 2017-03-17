from tests import BaseCase
from tests import dataset
# from api import preference_api
# from models import PreferenceModel
# from thirdparty import apriori
from api import mining_api


class MiningTestsBase(BaseCase):
    pass


class QueryRulesTests(MiningTestsBase):
    pass


class CreateRuleTests(MiningTestsBase):
    pass


class CreateRulesTests(MiningTestsBase):
    pass


class DeleteRulesTests(MiningTestsBase):
    pass


class DeleteRulesSince(MiningTestsBase):
    pass


class RunAprioriTests(MiningTestsBase):
    # TODO: This is more of an integration test
    def test_base(self):
        """
        Simple test to run the a priori algorhthim against our test shopping cart data
        and check results against expectations.
        """

        min_support = .2
        min_confidence = .7

        _, rule_models = mining_api.run_apriori(dataset.data2, min_support, min_confidence)

        # Check some expectations
        self.assertTrue(isinstance(rule_models, list))
        self.assertEqual(len(rule_models), 31)
        self.assertEqual(rule_models[0].__class__, mining_api.AssociationRuleModel)

        # Check a couple key results results
        rule1 = rule_models[9]
        self.assertEqual(rule1.ant, ['Jelly'])  # Single antecedant
        self.assertEqual(rule1.con, ['Peanut Butter', 'Bread'])  # Multiple consequents
        self.assertEqual(rule1.confidence, 0.8021978021978021)  # Non-0/1 confidence

        # Check a couple key results results
        rule2 = rule_models[-1]
        self.assertEqual(rule2.ant, ['Butter', 'Peanut Butter', 'Bread'])  # Multiple antecedant
        self.assertEqual(rule2.con, ['Jelly'])  # Single consequents
        self.assertEqual(rule2.confidence, 1.0)  # 100% confidence
