"""
Service level models

TODO: Keep ndb stuff out of here
"""


class PreferenceModel(object):
    """
    Lightweight object for representing a preference record
    """
    key = None
    user_id = None
    item_id = None
    pref = None
    timestamp = None
    synced_timestamp = None

    def __init__(self, user_id, item_id, pref, timestamp=None):
        self.user_id = user_id
        self.item_id = item_id
        self.pref = pref
        self.timestamp = timestamp
        self.key = self.generate_key()

    def generate_key(self):
        return "%s-%s" % (self.user_id, self.item_id)


class AssociationRule(object):
    """
    Model for representing an association Rule
    """
    key = None
    ant = []  # Antecedent
    con = None  # Consequent
    confidence = 0.0  # range of [0, 1]

    def __init__(self, ant, con, confidence):
        self.ant = ant
        self.con = con
        self.confidence = confidence

    def __repr__(self):
        return "Rule: %s ==> %s , %.3f" % (str(self.ant), str(self.con), self.confidence)
