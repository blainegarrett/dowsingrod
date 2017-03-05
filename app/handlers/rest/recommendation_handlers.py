import webapp2
from rest_core import handlers
from rest_core.resources import RestField
from rest_core.resources import BooleanField
from rest_core.resources import DatetimeField

from models import AssociationRule
from models import PreferenceModel

PREFERENCE_FIELDS = [
    # ResourceIdField(output_only=True),
    # ResourceUrlField(resource_url, output_only=True),
    RestField(PreferenceModel.user_id, required=True),
    RestField(PreferenceModel.item_id, required=True),
    BooleanField(PreferenceModel.pref, required=True),
    DatetimeField(PreferenceModel.timestamp),
    DatetimeField(PreferenceModel.synced_timestamp, output_only=True),
]

ASSOCIATION_RULES_FIELDS = [
    # ResourceIdField(output_only=True),
    # ResourceUrlField(resource_url, output_only=True),
    RestField(AssociationRule.user_id, required=True),
    RestField(AssociationRule.item_id, required=True),
    BooleanField(AssociationRule.pref, required=True),
    DatetimeField(AssociationRule.timestamp),
    DatetimeField(AssociationRule.synced_timestamp, output_only=True),
]


class RecommendationsHandler(handlers.RestHandlerBase):
    """
    Base Handler for Non-api calls
    """

    def get(self):
        raise Exception("bacon")


class RecordPreference(webapp2.RequestHandler):
    """
    Record a single preference
    """

    def get(self):  # TODO: Switch to post or put
        session_id = self.request.GET('session_id', None)  # session
        item_id = self.request.GET('item_id', None)  # artwork, gallery, etc
        pref = self.request.GET('pref', None)  # like or dislike
        timestamp = self.request.GET('timestamp', None)  # like or dislike

        # Construct a preference Model
        p = PreferenceModel(session_id, item_id, pref, timestamp=timestamp)

        # service.record_preference(p)

        raise Exception(session_id)
        self.response.write("Suggest endpoint")

"""
- Endpoints
- record pref
- record pref bulk


"""
