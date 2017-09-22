# API around Transaction Sets
from google.appengine.ext import ndb
from google.appengine.datastore.datastore_query import Cursor
from api.constants import DEFAULT_QUERY_LIMIT
from api.constants import BATCH_SIZE

from models import TransactionModel
from api.entities import PreferenceTransactionEntity
from rest_core.utils import get_resource_id_from_key


def query(cursor=None, *args, **kwargs):
    """
    Query for a set of preference item models
    Returns a 3-tuple of (domain models, opaque cursor str, bool more)
    """

    # Convert opaque cursor str to native appengine cursor
    if cursor:
        kwargs['cursor'] = Cursor(urlsafe=cursor)

    entities, next_cursor, more = _query_entities(*args, **kwargs)

    # Hydrate models to return to service layer
    models = []
    for e in entities:
        models.append(_populate_model(e))

    # Convert native cursor to opaque str
    if next_cursor:
        next_cursor = next_cursor.urlsafe()

    return models, next_cursor, more


def _query_entities(limit=DEFAULT_QUERY_LIMIT, cursor=None, *args, **kwargs):
    """
    Query for Transaction entities
    """

    if not limit:
        limit = DEFAULT_QUERY_LIMIT

    q = PreferenceTransactionEntity.query()
    # if (kwargs.get('user_id', None)):
    #    q = q.filter(PreferenceTransactionEntity.user_id == kwargs.get('user_id'))

    q = q.order(-PreferenceTransactionEntity.created_timestamp)

    entites, cursor, more = q.fetch_page(limit, start_cursor=cursor)
    return entites, cursor, more


def _populate_model(entity):
    model = TransactionModel()
    model.id = get_resource_id_from_key(entity.key)
    model.user_id = entity.user_id
    model.rule_item_ids = entity.rule_item_ids
    model.total_preferences = entity.total_preferences
    model.total_likes = entity.total_likes
    model.total_dislikes = entity.total_dislikes
    model.created_timestamp = entity.created_timestamp
    model.latest_timestamp = entity.latest_timestamp
    return model


def create_or_update_multi(user_id, pref_data_tuples):
    """
    """
    # Check if item exists
    txn_entity_key = ndb.Key('PreferenceTransactionEntity', user_id)
    entity = txn_entity_key.get()

    # Else: Populate a new one
    if not entity:
        entity = PreferenceTransactionEntity(key=txn_entity_key,
                                             total_preferences=0,
                                             total_likes=0,
                                             total_dislikes=0,
                                             user_id=user_id,
                                             rule_item_ids=[])
    delta_likes = 0
    delta_dislikes = 0
    delta_items = set()  # set
    for pref_data_tuple in pref_data_tuples:
        _, item_id, pref = pref_data_tuple  # Note: We don't care about user_id here

        # TODO: This is the same as PreferenceModel.PreferenceModel
        rule_item_id = '%s:%s' % (item_id, str(int(pref)))
        delta_items.add(rule_item_id)
        if (pref):
            delta_likes += 1
        else:
            delta_dislikes += 1

    # Update aspects of the item
    entity.total_preferences = int(entity.total_preferences) + (delta_likes + delta_dislikes)
    entity.total_likes = int(entity.total_likes) + delta_likes
    entity.total_dislikes = int(entity.total_dislikes) + delta_dislikes
    entity.rule_item_ids = list(set(entity.rule_item_ids).union(delta_items))

    entity.put()
    return entity


def get_txn_data():
    """
    Return a list of up to the latest 1000 sets of rule_key_ids to be used directly in the a priori

    eg a list of {'Peanut Butter:0', 'Beer:1', 'Jelly:1', Bread:2'}
    """

    next_cursor = None
    txn_sets_map = []
    more = True
    total_found = 0

    while(more and total_found < 1000):
        # Fetch data iterator for preference entities
        preference_entities, next_cursor, more = _query_entities(limit=BATCH_SIZE,
                                                                 cursor=next_cursor)
        for pref in preference_entities:
            txn_sets_map.append(set(pref.rule_item_ids))

        total_found += 1
    return txn_sets_map
