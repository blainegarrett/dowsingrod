"""
Internal Api for Data Mining Persistance
"""

from google.appengine.ext import ndb

from thirdparty import apriori as apriori

from api.entities import AssociationRuleEntity


def query_rules():
    """
    Query for a set of AssociationRuleEntities
    # TODO: Filtering, etc
    """

    return AssociationRuleEntity.query().all()


def create_rule(model):
    """
    Persist a single association rule
    """

    e = _populate_entity(model)
    e.put()

    model.created_timestamp = e.created_timestamp
    return model


def create_rules(models):
    """
    Persist a list of association rules
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
        rule_entity = AssociationRuleEntity()
        rule_entity.ant = list(r_set[0][0])  # was a frozen set
        rule_entity.con = list(r_set[0][1])  # was a frozen set
        rule_entity.confidence = r_set[1]
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


def _populate_entity(model):
    """
    Populate a ndb entity from a model
    """

    # TODO: If we support a key, use it

    data = {'ant': model.ant,
            'con': model.con,
            'confidence': model.confidence
            }

    e = AssociationRuleEntity(**data)

    return e
