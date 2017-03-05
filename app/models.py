"""
Service level models

TODO: Keep ndb stuff out of here
"""

# Base model class
from google.appengine.ext import ndb
from rest_core.models import Model

# TODO: Eventually re-work this so it doesn't extend ndb.Model


class PreferenceModel(Model):
    """
    Lightweight object for representing a preference record
    """
    user_id = ndb.StringProperty()
    item_id = ndb.StringProperty()
    pref = ndb.BooleanProperty()
    timestamp = ndb.DateTimeProperty()
    synced_timestamp = ndb.DateTimeProperty()

    def __init__(self, user_id, item_id, pref, timestamp=None):
        super(Model, self).__init__()

        self.user_id = user_id
        self.item_id = item_id
        self.pref = pref
        self.timestamp = timestamp


    def generate_key(self):
        return "%s-%s" % (self.user_id, self.item_id)

# TODO: Rename AssociationRuleModel


class AssociationRule(Model):
    """
    Model for representing an association Rule
    """
    ant = ndb.StringProperty(repeated=True)  # Antecedent
    con = ndb.StringProperty(repeated=True)  # Consequent
    confidence = ndb.FloatProperty(repeated=True)  # range of [0, 1]

    def __init__(self, ant, con, confidence):
        super(Model, self).__init__()

        self.ant = ant
        self.con = con
        self.confidence = confidence

    def __repr__(self):
        return "Rule: %s ==> %s , %.3f" % (str(self.ant), str(self.con), self.confidence)
