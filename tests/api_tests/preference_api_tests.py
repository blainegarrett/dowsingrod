from tests import BaseCase
from api import preference_api
from models import PreferenceModel


class PreferenceTestsBase(BaseCase):
    def setUp(self):

        super(PreferenceTestsBase, self).setUp()

        p0 = preference_api.PreferenceEntity(user_id='u1', item_id='Peanut Butter', pref=False)
        p1 = preference_api.PreferenceEntity(user_id='u2', item_id='Peanut Butter', pref=True)
        preference_api.create_multi([p0, p1])


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


class CreateTest(PreferenceTestsBase):
    def test_base(self):
        t = None  # TODO: Miliseconds
        p0 = PreferenceModel('u1', 'i1', True, t)
        result = preference_api.create(p0)
        self.assertEqual(result, p0)


class CreateMultiTest(PreferenceTestsBase):
    def test_base(self):
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

        self.assertTrue(isinstance(result[1], PreferenceModel))
        self.assertEqual(result[1].user_id, 'u2')
        self.assertEqual(result[1].item_id, 'i2')
        self.assertEqual(result[1].pref, False)
        self.assertEqual(result[1].timestamp, t1)


class QueryEntitiesTests(PreferenceTestsBase):
    def test_base(self):
        """
        Simple test to ensure we query for all existing preference entities
        """
        entities = preference_api.query_preference_entities()
        self.assertEqual(len(entities), 2)
        self.assertTrue(isinstance(entities[0], preference_api.PreferenceEntity))
        self.assertTrue(isinstance(entities[1], preference_api.PreferenceEntity))


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
