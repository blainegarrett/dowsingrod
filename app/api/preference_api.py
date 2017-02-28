"""
Low level API surrounding preferences persistance
"""
from google.appengine.ext import ndb
from api.entities import PreferenceEntity


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

    # TODO: Rehydrate key and sync_timestamp
    return models


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
