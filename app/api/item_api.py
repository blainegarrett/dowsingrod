from google.appengine.ext import ndb
from google.appengine.datastore.datastore_query import Cursor
from api.constants import DEFAULT_QUERY_LIMIT
from api.entities import PreferenceItemEntity
from rest_core.utils import get_resource_id_from_key
from models import ItemModel


def get_by_item_ids(item_ids):
    """
    Fetch a list of Item Models by their item_id
    TODO: Sort by total_preferences reverse
    """

    keys = []
    for item_id in item_ids:
        if (item_id):
            keys.append(ndb.Key('PreferenceItemEntity', item_id))
        else:
            keys.append(ndb.Key('PreferenceItemEntity', 'doesNotExist'))

    entities = ndb.get_multi(keys)

    # Hydrate models to return to service layer
    models = []
    for e in entities:
        models.append(_populate_model(e))
    return models


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
    Query for preference entities
    """

    if not limit:
        limit = DEFAULT_QUERY_LIMIT

    q = PreferenceItemEntity.query()
    if (kwargs.get('user_id', None)):
        q = q.filter(PreferenceItemEntity.user_id == kwargs.get('user_id'))

    q = q.order(-PreferenceItemEntity.created_timestamp)

    entites, cursor, more = q.fetch_page(limit, start_cursor=cursor)
    return entites, cursor, more


def _populate_model(entity):

    if not entity:
        return None

    model = ItemModel()
    model.id = get_resource_id_from_key(entity.key)
    model.item_id = entity.item_id
    model.user_ids = entity.user_ids
    model.total_likes = entity.total_likes
    model.total_dislikes = entity.total_dislikes
    model.total_preferences = entity.total_preferences
    model.created_timestamp = entity.created_timestamp
    model.latest_timestamp = entity.latest_timestamp
    return model


def create_or_update_multi(item_id, pref_data_tuples):
    """
    """
    # Check if item exists
    item_entity_key = ndb.Key('PreferenceItemEntity', item_id)
    entity = item_entity_key.get()

    # Else: Populate a new one
    if not entity:
        entity = PreferenceItemEntity(key=item_entity_key,
                                      item_id=item_id,
                                      total_preferences=0,
                                      total_likes=0,
                                      total_dislikes=0,
                                      user_ids=[])

    delta_likes = 0
    delta_dislikes = 0
    delta_users = set()  # set
    for pref_data_tuple in pref_data_tuples:
        user_id, _, pref = pref_data_tuple  # Note: We don't care about item_id here

        delta_users.add(user_id)
        if (pref):
            delta_likes += 1
        else:
            delta_dislikes += 1

    # Update aspects of the item
    entity.total_preferences = int(entity.total_preferences) + (delta_likes + delta_dislikes)

    if (pref):
        entity.total_likes = int(entity.total_likes) + delta_likes
    else:
        entity.total_dislikes = int(entity.total_dislikes) + delta_dislikes

    entity.user_ids = list(set(entity.user_ids).union(delta_users))

    entity.put()
    return entity

