from tests import BaseCase
from services import preference_service
from models import PreferenceModel


class PreferenceServiceTestsBase(BaseCase):
    pass


class CreateMultiTest(PreferenceServiceTestsBase):
    def test_base(self):
        t1 = None  # TODO: Miliseconds
        t2 = None  # TODO: Miliseconds

        p0 = PreferenceModel('u1', 'i1', True, t1)
        p1 = PreferenceModel('u2', 'i2', False, t2)
        result = preference_service.record_preference([p0, p1])
        self.assertEqual(result, [p0, p1])
