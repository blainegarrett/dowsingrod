from mock import patch
import datetime
from tests import BaseCase
from api import preference_api
from models import PreferenceModel

BDAY_TUPLE = (1982, 9, 2, 16, 30, 0)  # Blane's birthday


class PreferenceTestsBase(BaseCase):
    pass


class EntityTests(PreferenceTestsBase):
    def test_get_rule_item_id(self):
        """
        Ensure we can generate a composite pref id for use in txn lists
        representing item and if the session user liked it or not.
        """

        p1 = preference_api.PreferenceEntity(user_id='u1', item_id='Peanut Butter', pref=False)
        p2 = preference_api.PreferenceEntity(user_id='u2', item_id='Peanut Butter', pref=True)

        self.assertEqual(p1.get_rule_item_id(), 'Peanut Butter:0')
        self.assertEqual(p2.get_rule_item_id(), 'Peanut Butter:1')


@patch('api.preference_api.get_resource_id_from_key', return_value='mocked_id')
class CreateTest(PreferenceTestsBase):
    """Tests around creating a single Preferece"""

    def test_base(self, m_get_id):
        t = datetime.datetime(*BDAY_TUPLE)
        p0 = PreferenceModel('u3', 'i3', False, t)
        result = preference_api.create(p0)

        self.assertTrue(isinstance(result, PreferenceModel))
        self.assertEqual(result.user_id, 'u3')
        self.assertEqual(result.item_id, 'i3')
        self.assertEqual(result.pref, False)
        self.assertEqual(result.timestamp, t)
        self.assertTrue(result.synced_timestamp is not None)
        self.assertEquals(result.id, 'mocked_id')


@patch('api.preference_api.get_resource_id_from_key', return_value='mocked_id')
class CreateMultiTest(PreferenceTestsBase):
    """Tests around creating multiple preferences at once"""
    def test_base(self, m_get_id):
        t1 = None  # TODO: Miliseconds
        t2 = None  # TODO: Miliseconds

        p0 = PreferenceModel('u1', 'i1', True, t1)
        p1 = PreferenceModel('u2', 'i2', False, t2)
        result = preference_api.create_multi([p0, p1])

        self.assertTrue(isinstance(result, list))

        self.assertTrue(isinstance(result[0], PreferenceModel))
        self.assertEqual(result[0].user_id, 'u1')
        self.assertEqual(result[0].item_id, 'i1')
        self.assertEqual(result[0].pref, True)
        self.assertEqual(result[0].timestamp, t1)
        self.assertTrue(result[0].synced_timestamp is not None)
        self.assertEquals(result[0].id, 'mocked_id')

        self.assertTrue(isinstance(result[1], PreferenceModel))
        self.assertEqual(result[1].user_id, 'u2')
        self.assertEqual(result[1].item_id, 'i2')
        self.assertEqual(result[1].pref, False)
        self.assertEqual(result[1].timestamp, t1)
        self.assertTrue(result[1].synced_timestamp is not None)
        self.assertEquals(result[1].id, 'mocked_id')

        self.assertEqual(m_get_id.call_count, 2)


class QueryEntitiesTests(PreferenceTestsBase):
    """Tests around query for preferences"""

    def setUp(self):

        super(QueryEntitiesTests, self).setUp()

        p0 = preference_api.PreferenceEntity(user_id='u1', item_id='Peanut Butter', pref=False,
                                             timestamp=datetime.datetime(*BDAY_TUPLE))
        p1 = preference_api.PreferenceEntity(user_id='u2', item_id='Peanut Butter', pref=True,
                                             timestamp=None)
        preference_api.create_multi([p0, p1])

    def test_no_params(self):
        """
        Simple test to ensure we query for all existing preference entities
        """
        entities, cursor, more = preference_api._query_preference_entities()
        self.assertEqual(len(entities), 2)
        self.assertTrue(isinstance(entities[0], preference_api.PreferenceEntity))
        self.assertTrue(isinstance(entities[1], preference_api.PreferenceEntity))


class QueryModelsTests(PreferenceTestsBase):
    @patch('api.preference_api._query_preference_entities')
    @patch('api.preference_api._populate_model')
    def test_base(self, mock_populate, mock_query):
        # Setup Mocks
        mock_query.return_value = (['a', 'b'], None, False)

        # Run Code To Test
        models, cursor, more = preference_api.query_preference_models(limit=4, kwarg=True)

        # Check results
        self.assertEqual(models, [mock_populate.return_value, mock_populate.return_value])
        mock_query.assert_called_once_with(limit=4, kwarg=True)


class GetTxnDataTests(PreferenceTestsBase):
    def setUp(self):

        super(GetTxnDataTests, self).setUp()

        p0 = preference_api.PreferenceEntity(user_id='u1', item_id='Peanut Butter', pref=False)
        p1 = preference_api.PreferenceEntity(user_id='u2', item_id='Peanut Butter', pref=True)
        p2 = preference_api.PreferenceEntity(user_id='u3', item_id='Bacon', pref=False)
        p3 = preference_api.PreferenceEntity(user_id='u1', item_id='Jelly', pref=True)
        p4 = preference_api.PreferenceEntity(user_id='u1', item_id='Steak', pref=False)
        preference_api.create_multi([p0, p1, p2, p3, p4])

    def test_base(self):
        """
        Test behavior of grouping individual preferences into user transactions
        """
        result_sets = preference_api.get_txn_data()

        u1_expected = set([u'Jelly:1', u'Peanut Butter:0', u'Steak:0'])
        u2_expected = set([u'Bacon:0'])
        u3_expected = set([u'Peanut Butter:1'])

        self.assertTrue(u1_expected in result_sets)
        self.assertTrue(u2_expected in result_sets)
        self.assertTrue(u3_expected in result_sets)
