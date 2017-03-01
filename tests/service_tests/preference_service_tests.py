from tests import BaseCase
from services import preference_service
from models import PreferenceModel
from thirdparty import dataset


class PreferenceServiceTestsBase(BaseCase):
    pass


class CreateMultiTests(PreferenceServiceTestsBase):
    def test_base(self):
        t1 = None  # TODO: Miliseconds
        t2 = None  # TODO: Miliseconds

        p0 = PreferenceModel('u1', 'i1', True, t1)
        p1 = PreferenceModel('u2', 'i2', False, t2)
        result = preference_service.record_preference([p0, p1])
        self.assertEqual(result, [p0, p1])


class TestGenerateAssociationRules(PreferenceServiceTestsBase):
    def setUp(self):
        super(TestGenerateAssociationRules, self).setUp()

    def test_base(self):
        """
        TODO: This acts as an integration test
        """

        u = 0
        models_to_put = []
        for txn in dataset.data2:
            u += 1
            for txn_item in txn:
                models_to_put.append(PreferenceModel("user%s" % u, txn_item, True))
        preference_service.record_preference(models_to_put)

        min_support = .2
        min_confidence = .7

        result = preference_service.generate_association_rules(min_support, min_confidence)

        for r in result:
            print r
