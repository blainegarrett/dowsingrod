from google.appengine.ext import ndb


class PreferenceEntity(ndb.Model):
    """ Persistance model to Appengine NDB datastore for a preference recording """

    user_id = ndb.StringProperty()  # Session/Vistor Id
    item_id = ndb.StringProperty()  # Id of Artwork/Gallery whatever being recorded
    pref = ndb.BooleanProperty()  # True = Like, #False = Dislike
    timestamp = ndb.DateTimeProperty()  # Timestamp of preference recorded on device

    synced_timestamp = ndb.DateTimeProperty(auto_now_add=True)  # Timestamp when pref synced


class AssociationRuleEntity(ndb.Model):
    """ Persistance model for association rule """
    ant = ndb.StringProperty(repeated=True)  # antecedent
    con = ndb.StringProperty(repeated=True)  # Confidence
    confidence = ndb.FloatProperty()  # range of [0, 1]
    created_timestamp = ndb.DateTimeProperty(auto_now_add=True)  # Timestamp when pref synced

    def __repr__(self):
        return "Rule: %s ==> %s , %.3f" % (str(self.ant), str(self.con), self.confidence)
