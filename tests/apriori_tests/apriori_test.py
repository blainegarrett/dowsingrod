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
    def test_base(self):

        # txn_models = []
        min_support = .2
        min_confidence = .3

        _, rule_models = mining_api.run_apriori(dataset.data2, min_support, min_confidence)

        raise Exception(rule_models)
