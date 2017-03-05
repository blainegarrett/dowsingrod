"""
Low level API surrounding preferences persistance
"""
from google.appengine.ext import ndb
from api.entities import PreferenceEntity
from models import PreferenceModel


def create(model):
    """
    Persist preference based on input model
    """
    e = _populate_entity(model)
    e.put()

    model.synced_timestamp = e.synced_timestamp
    return model


def create_multi(models):
    """
    Persist a list of preference models
    """

    # Convert all models into entities
    entities_to_put = []
    for model in models:
        entities_to_put.append(_populate_entity(model))

    # Bulk persist entities
    # entity_keys = ndb.put_multi(entities_to_put)
    ndb.put_multi(entities_to_put)

    return_models = []
    for e in entities_to_put:
        return_models.append(_populate_model(e))

    return return_models


def _populate_model(entity):
    """
    Populate a model from an ndb entity
    """

    # TODO: If we support a key, use it
    m = PreferenceModel(entity.user_id, entity.item_id, entity.pref, entity.timestamp)
    m.synced_timestamp = entity.synced_timestamp
    return m


def _populate_entity(model):
    """
    Populate a ndb entity from a model
    """

    # TODO: If we support a key, use it

    data = {'user_id': model.user_id,
            'item_id': model.item_id,
            'pref': model.pref,
            'timestamp': model.timestamp
            }

    e = PreferenceEntity(**data)

    return e


def query_preference_entities():
    """
    Query for preference entities
    """
    # TODO: Beef this up quite a bit
    # TODO: Conditionally case to Models...
    return PreferenceEntity.query().fetch(1000)


def get_txn_data():
    """
    Query for all preferences and group into transaction list format

    {'session_id': ['Peanut Butter', 'Beer', 'Jelly', Bread']}
    """

    txn_sets_map = {}

    # Fetch data iterator for preference entities
    preference_entities = query_preference_entities()

    for pref in preference_entities:
        if pref.user_id not in txn_sets_map:
            txn_sets_map[pref.user_id] = set()
        txn_sets_map[pref.user_id].add(pref.get_rule_item_id())

    return txn_sets_map.values()
