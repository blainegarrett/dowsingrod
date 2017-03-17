"""
Internal Api for Data Mining Persistance
"""

from google.appengine.ext import ndb

from thirdparty import apriori as apriori

from api.entities import AssociationRuleEntity
from api.entities import AssociationRuleSetEntity

from models import AssociationRuleSetModel
from models import AssociationRuleModel
from rest_core.utils import get_resource_id_from_key  # , get_key_from_resource_id

# Association RuleSets


def _query_ruleset_entities(*args, **kwargs):
    # TODO: Add support for filters, etc

    q = AssociationRuleSetEntity.query()
    q = q.order(-AssociationRuleSetEntity.created_timestamp)
    return q.fetch(1000)


def query_ruleset_models(*args, **kwargs):
    """
    Query for a set of AssociationRuleSet Models
    TODO: Needs pagination, search terms, etc
    """
    entities = _query_ruleset_entities(*args, **kwargs)

    # Hydrate models to return to service layer
    models = []
    for e in entities:
        models.append(_populate_ruleset_model(e))
    return models


def _populate_ruleset_model(entity):
    m = AssociationRuleSetModel(entity.min_support, entity.min_confidence)
    m.created_timestamp = entity.created_timestamp
    m.total_rules = entity.total_rules
    m.id = get_resource_id_from_key(entity.key)
    return m


def create_ruleset(min_support, min_confidence):
    # TODO: Move to api layer
    e = AssociationRuleSetEntity()
    e.min_support = min_support
    e.min_confidence = min_confidence
    e.put()

    return _populate_ruleset_model(e)


# Association rules

def query_rule_models(*args, **kwargs):
    """
    Query for a set of AssociationRule Models
    TODO: Needs pagination, search terms, etc
    """
    entities = _query_rule_entities(*args, **kwargs)

    # Hydrate models to return to service layer
    models = []
    for e in entities:
        models.append(_populate_rule_model(e))

    return models


def _query_rule_entities(*args, **kwargs):
    """
    Query for preference entities
    """
    # TODO: Beef this up quite a bit
    # TODO: Conditionally case to Models...
    # TODO: This doesn't currently have unit tests around it

    q = AssociationRuleEntity.query()
    if (kwargs.get('ruleset_id', None)):
        q = q.filter(AssociationRuleEntity.ruleset_id == kwargs.get('ruleset_id'))

    # Sorting
    entities = q.fetch(1000)
    return entities


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
    """
    ndb.delete_multi(
        AssociationRuleEntity.query().filter(AssociationRuleEntity.created_timestamp < timestamp).iter(keys_only=True)
    )
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
