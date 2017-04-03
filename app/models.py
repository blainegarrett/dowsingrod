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

    def get_rule_item_id(self):
        # TODO: This is duplicated on the entity
        return '%s:%s' % (self.item_id, str(int(self.pref)))


class AssociationRuleSetModel(Model):
    """Persistance model to Appengine to Store a association rule set"""
    min_confidence = ndb.FloatProperty()
    min_support = ndb.FloatProperty()
    total_rules = ndb.IntegerProperty()
    created_timestamp = ndb.DateTimeProperty()

    def __init__(self, min_support, min_confidence):
        super(Model, self).__init__()

        self.min_confidence = min_confidence
        self.min_support = min_support


class AssociationRuleModel(Model):
    """
    Model for representing an association Rule
    """
    ant = ndb.StringProperty(repeated=True)  # Antecedent
    con = ndb.StringProperty(repeated=True)  # Consequent
    confidence = ndb.FloatProperty()  # range of [0, 1]
    rule_key = ndb.StringProperty()
    ruleset_id = ndb.StringProperty()

    def __init__(self, ant, con, confidence):
        super(Model, self).__init__()

        self.ant = ant
        self.con = con
        self.confidence = confidence
        self.rule_key = self.generate_rule_key()

    def __repr__(self):
        return "Rule: %s ==> %s , %.3f" % (str(self.ant), str(self.con), self.confidence)

    def generate_rule_key(self):
        """
        Generate an identifier for a rule key based on the antecedant items
        """

        # General cleanup
        cleaned_items = []
        for item in self.ant:
            cleaned_items.append(item.lower().replace(' ', '_'))

        # Sort
        cleaned_items.sort()

        # Concat them together
        return '__'.join(cleaned_items)
