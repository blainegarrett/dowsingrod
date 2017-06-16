"""
Internal Api for Data Mining Persistance
"""

from google.appengine.ext import ndb
from google.appengine.datastore.datastore_query import Cursor

from thirdparty import apriori as apriori

from api.entities import AssociationRuleEntity
from api.entities import AssociationRuleSetEntity

from models import AssociationRuleSetModel
from models import AssociationRuleModel

from api.constants import DEFAULT_QUERY_LIMIT

from rest_core.utils import get_resource_id_from_key, get_key_from_resource_id

# Association RuleSets


def get_ruleset_by_id(ruleset_id):
    # TODO: Ensure that this is of type AssociationRuleSet
    # TODO: Unit test
    key = get_key_from_resource_id(ruleset_id)
    e = key.get()
    return _populate_ruleset_model(e)


def _query_ruleset_entities(limit=DEFAULT_QUERY_LIMIT, cursor=None, *args, **kwargs):
    if not limit:
        limit = DEFAULT_QUERY_LIMIT

    q = AssociationRuleSetEntity.query()
    q = q.order(-AssociationRuleSetEntity.created_timestamp)

    entites, cursor, more = q.fetch_page(limit, start_cursor=cursor)
    return entites, cursor, more


def query_ruleset_models(cursor=None, *args, **kwargs):
    """
    Query for a set of AssociationRuleSet Models
    Returns a 3-tuple of (domain models, opaque cursor str, bool more)
    """

    # Convert opaque cursor str to native appengine cursor
    if cursor:
        kwargs['cursor'] = Cursor(urlsafe=cursor)

    entities, next_cursor, more = _query_ruleset_entities(*args, **kwargs)

    # Hydrate models to return to service layer
    models = []
    for e in entities:
        models.append(_populate_ruleset_model(e))

    # Convert native cursor to opaque str
    if next_cursor:
        next_cursor = next_cursor.urlsafe()

    return models, next_cursor, more


def _populate_ruleset_model(entity):
    m = AssociationRuleSetModel(entity.min_support, entity.min_confidence)
    m.created_timestamp = entity.created_timestamp
    m.total_rules = entity.total_rules
    m.id = get_resource_id_from_key(entity.key)
    return m


def _populate_ruleset_entity(model):
    """
    Populate a ndb entity from a model
    """
    data = {
        'min_support': model.min_support,
        'min_confidence': model.min_support,
        'created_timestamp': model.created_timestamp,
        'total_rules': model.total_rules,
    }

    if model.id:
        data['key'] = get_key_from_resource_id(model.id)
    return AssociationRuleSetEntity(**data)


def create_ruleset(min_support, min_confidence):
    # TODO: Move to api layer
    e = AssociationRuleSetEntity()
    e.min_support = min_support
    e.min_confidence = min_confidence
    e.put()

    return _populate_ruleset_model(e)


# Association rules

def query_rule_models(cursor=None, *args, **kwargs):
    """
    Query for a set of AssociationRule Models
    Returns a 3-tuple of (domain models, opaque cursor str, bool more)
    """

    # Convert opaque cursor str to native appengine cursor
    if cursor:
        kwargs['cursor'] = Cursor(urlsafe=cursor)

    entities, next_cursor, more = _query_rule_entities(*args, **kwargs)

    # Hydrate models to return to service layer
    models = []
    for e in entities:
        models.append(_populate_rule_model(e))

    # Convert native cursor to opaque str
    if next_cursor:
        next_cursor = next_cursor.urlsafe()

    return models, next_cursor, more


def _query_rule_entities(limit=DEFAULT_QUERY_LIMIT, cursor=None, *args, **kwargs):
    """
    Query for preference entities
    """
    # TODO: This doesn't currently have unit tests around it ?

    if not limit:
        limit = DEFAULT_QUERY_LIMIT

    q = AssociationRuleEntity.query()
    if (kwargs.get('ruleset_id', None)):
        q = q.filter(AssociationRuleEntity.ruleset_id == kwargs.get('ruleset_id'))

    q = q.order(-AssociationRuleEntity.confidence)

    entites, cursor, more = q.fetch_page(limit, start_cursor=cursor)
    return entites, cursor, more


def create_rule(ruleset_id, model):
    """
    Persist a single association rule
    """

    e = _populate_rule_entity(model)
    e.ruleset_id = ruleset_id
    e.put()

    # Hydrate model to return to service layer
    model = _populate_rule_model(e)
    return model


def create_rules(ruleset_id, models):
    """
    Persist a list of association rules
    """

    # Convert all models into entities
    entities_to_put = []
    for model in models:
        e = _populate_rule_entity(model)
        e.ruleset_id = ruleset_id
        entities_to_put.append(e)

    # Bulk persist entities
    # entity_keys = ndb.put_multi(entities_to_put)
    ndb.put_multi(entities_to_put)

    # Hydrate models to return to service layer
    return_models = []
    for e in entities_to_put:
        return_models.append(_populate_rule_model(e))

    return return_models


def delete_rules():
    """
    Batch Delete all association rules
    """
    ndb.delete_multi(
        AssociationRuleEntity.query().iter(keys_only=True)
    )
    return True


def delete_rules_since(timestamp):
    """
    Batch Delete rules older than timestamp
    TODO: Determine if this is cruft
    """
    ndb.delete_multi(AssociationRuleEntity.query().filter(AssociationRuleEntity.created_timestamp < timestamp).iter(keys_only=True))
    return True


def run_apriori(data_iter, min_support, min_confidence):
    """
    Run the a priori algorithm and return the applicable item_models & generated association rules
    """

    # Run 3rd party a priori algorithm
    item_sets, rule_sets = apriori.runApriori(data_iter, min_support, min_confidence)

    # Iterate of rules in frozen set form and
    rule_entities = []
    for r_set in rule_sets:
        rule_entity = AssociationRuleModel(list(r_set[0][0]), list(r_set[0][1]), r_set[1])
        rule_entities.append(rule_entity)

    # Debug results
    _print_items_and_rules(item_sets, rule_entities)

    item_models = item_sets

    return item_models, rule_entities


def _print_items_and_rules(items, rule_entities):
    """
    """
    return

    for item, support in sorted(items, key=lambda (item, support): support):
        print "item: %s , %.3f" % (str(item), support)

    print "\n------------------------ RULES:"

    for r in rule_entities:
        print r


def _populate_rule_model(entity):
    m = AssociationRuleModel(entity.ant, entity.con, entity.confidence)
    m.id = get_resource_id_from_key(entity.key)
    m.ruleset_id = entity.ruleset_id
    return m


def _populate_rule_entity(model):
    """
    Populate a ndb entity from a model
    """

    # TODO: If we support a key, use it
    data = {'rule_key': model.generate_rule_key(),
            'ant': model.ant,
            'con': model.con,
            'confidence': model.confidence
            }

    return AssociationRuleEntity(**data)
