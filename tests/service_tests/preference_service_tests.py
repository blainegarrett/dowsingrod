from mock import patch
from tests import BaseCase
from services import preference_service
from models import PreferenceModel
from tests import dataset


class PreferenceServiceTestsBase(BaseCase):
    pass


class RecordPreferenceTests(PreferenceServiceTestsBase):
    def test_multiple(self):
        t1 = None  # TODO: Miliseconds
        t2 = None  # TODO: Miliseconds

        p0 = PreferenceModel('u1', 'i1', True, t1)
        p1 = PreferenceModel('u2', 'i2', False, t2)
        result = preference_service.record_preference([p0, p1])

        self.assertTrue(isinstance(result, list))

        self.assertTrue(isinstance(result[0], PreferenceModel))
        self.assertEqual(result[0].user_id, 'u1')
        self.assertEqual(result[0].item_id, 'i1')
        self.assertEqual(result[0].pref, True)
        self.assertEqual(result[0].timestamp, t1)

        self.assertTrue(isinstance(result[1], PreferenceModel))
        self.assertEqual(result[1].user_id, 'u2')
        self.assertEqual(result[1].item_id, 'i2')
        self.assertEqual(result[1].pref, False)
        self.assertEqual(result[1].timestamp, t1)

    def test_single(self):
        t1 = None  # TODO: Miliseconds

        p0 = PreferenceModel('u1', 'i1', True, t1)
        result = preference_service.record_preference(p0)

        self.assertTrue(isinstance(result, PreferenceModel))
        self.assertEqual(result.user_id, 'u1')
        self.assertEqual(result.item_id, 'i1')
        self.assertEqual(result.pref, True)
        self.assertEqual(result.timestamp, t1)


class TestGenerateAssociationRules(PreferenceServiceTestsBase):

    def setUp(self):
        super(TestGenerateAssociationRules, self).setUp()

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

        result = preference_service.generate_association_rules(min_support, min_confidence)

        self.assertEqual(len(result), 31)
        self.assertEqual(result[0].ant, [u'Butter:1'])
        self.assertEqual(result[0].con, [u'Peanut Butter:1'])
        self.assertEqual(result[0].confidence, 1.0)


class QueryPreferencesTests(PreferenceServiceTestsBase):
    @patch('api.preference_api.query_preference_models')
    def test_base(self, mock_api):
        """
        This test exists just for coverage. Revisit once we add full support
        """
        result = preference_service.query_preferences('arg', some='kwarg')
        self.assertEquals(result, mock_api.return_value)
        mock_api.assert_called_once_with('arg', some='kwarg')


class GetByIdTests(PreferenceServiceTestsBase):
    @patch('api.preference_api.get_model_by_id')
    def test_base(self, mock_api):
        result = preference_service.get_by_id('some_id')
        self.assertEquals(result, mock_api.return_value)
        mock_api.assert_called_once_with('some_id')
