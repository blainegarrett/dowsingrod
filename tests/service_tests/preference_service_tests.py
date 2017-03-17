from mock import patch
from tests import BaseCase
from services import preference_service
from models import PreferenceModel


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
