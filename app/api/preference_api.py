"""
Low level API surrounding preferences persistance
Keep all persistance implementation in this layer and return models to service layer
"""
from google.appengine.ext import ndb
from api.entities import PreferenceEntity
from models import PreferenceModel
from rest_core.utils import get_resource_id_from_key, get_key_from_resource_id


def get_model_by_id(id):
    """
    Get a domain model by id
    """
    e = _get_by_id(id)
    if not e:
        return None
    return _populate_model(e)


def create(model):
    """
    Persist preference based on input model
    """
    e = _populate_entity(model)
    e.put()

    # Hydrate model to return to service layer
    model = _populate_model(e)
    return model


def create_multi(models):
    """
    Persist a list of preference models
    Note: This is not currently transactional and doesn't batch puts()
    """

    # Convert all models into entities
    entities_to_put = []
    for model in models:
        entities_to_put.append(_populate_entity(model))

    # Bulk persist entities
    ndb.put_multi(entities_to_put)

    # Hydrate models to return to service layer
    return_models = []
    for e in entities_to_put:
        return_models.append(_populate_model(e))

    return return_models


def _get_by_id(id):
    try:
        key = get_key_from_resource_id(id)
        return key.get()
    except (TypeError, ValueError):
        return None


def _populate_model(entity):
    """
    Populate a model from an ndb entity
    """

    m = PreferenceModel(entity.user_id, entity.item_id, entity.pref, entity.timestamp)
    m.synced_timestamp = entity.synced_timestamp
    m.id = get_resource_id_from_key(entity.key)
    return m


def _populate_entity(model):
    """
    Populate a ndb entity from a model
    TODO: This doesn't currently support setting key on create
    """
    data = {'user_id': model.user_id,
            'item_id': model.item_id,
            'pref': model.pref,
            }

    # NDB Models are expected to be in timezone unaware format - implicit UTC
    if model.timestamp:
        data['timestamp'] = model.timestamp.replace(tzinfo=None)

    return PreferenceEntity(**data)


def query_preference_models(*args, **kwargs):
    """
    Query for a set of collection models
    TODO: Needs pagination, search terms, etc
    """
    entities = _query_preference_entities(*args, **kwargs)

    # Hydrate models to return to service layer
    models = []
    for e in entities:
        models.append(_populate_model(e))

    return models


def _query_preference_entities(*args, **kwargs):
    """
    Query for preference entities
    """
    # TODO: Beef this up quite a bit
    # TODO: Conditionally case to Models...
    # TODO: This doesn't currently have unit tests around it

    q = PreferenceEntity.query()
    if (kwargs.get('user_id', None)):
        q = q.filter(PreferenceEntity.user_id == kwargs.get('user_id'))

    q = q.order(-PreferenceEntity.synced_timestamp)
    entities = q.fetch(1000)
    return entities


def get_txn_data():
    """
    Query for all preferences and group into transaction list format

    {'session_id': ['Peanut Butter:0', 'Beer:1', 'Jelly:1', Bread:2']}
    """

    txn_sets_map = {}

    # Fetch data iterator for preference entities
    preference_entities = _query_preference_entities()

    for pref in preference_entities:
        if pref.user_id not in txn_sets_map:
            txn_sets_map[pref.user_id] = set()
        txn_sets_map[pref.user_id].add(pref.get_rule_item_id())

    return txn_sets_map.values()
