from tests import BaseCase
from api import preference_api
from models import PreferenceModel


class PreferenceTestsBase(BaseCase):
    pass


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
        self.assertEqual(result, [p0, p1])
