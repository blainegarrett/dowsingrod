from google.appengine.ext import ndb  # TODO: Refactor this out
from api import mining_api
from api import preference_api
from furious.async import Async
import logging


def query_rules(*args, **kwargs):
    """
    TODO: Support filters, paginations, etc
    """
    return mining_api.query_rule_models(*args, **kwargs)


def get_rule_set(ruleset_id):
    return mining_api.get_ruleset_by_id(ruleset_id)


def query_rule_sets(*arga, **kwargs):
    return mining_api.query_ruleset_models(*arga, **kwargs)


def delete_rules():
    """
    Delete Rules
    TODO: May simply want to flag them as not the current set
    """
    return mining_api.delete_rules()


def generate_association_rules_async(ruleset_id, min_support, min_confidence, make_default):
    logging.info("Enqueuing generate_association_rules")
    async = Async(target='services.rule_service.generate_association_rules',
                  args=(ruleset_id, min_support, min_confidence, make_default))
    async.start()


def generate_association_rules(ruleset_id, min_support, min_confidence, make_default):
    """
    Process to generate association rules
    """
    # TODO: This probably needs to be split up into separate async functions
    # TODO: It feels weird importing the pref_api, but we need the prefs in our specific format
    log_args = (ruleset_id, min_support, min_confidence)
    logging.info("Starting Generation of Ruleset with id %s - %s - %s " % log_args)

    txn_data = preference_api.get_txn_data()

    # TODO: Create an association_rule entity

    ruleset_model, rule_models = mining_api.run_apriori(txn_data, min_support, min_confidence)
    rule_models = mining_api.create_rules(ruleset_id, rule_models)

    # Update rule model with total count
    ruleset_model = mining_api.get_ruleset_by_id(ruleset_id)

    # TODO: THIS SHOULD HAPPEN in the api layer
    ruleset_model.total_rules = len(rule_models)
    if make_default:
        designate_default(ruleset_model)
    else:
        e = mining_api._populate_ruleset_entity(ruleset_model)
        e.put()

    logging.info("Completing generation of Ruleset with id %s - %s - %s " % log_args)
    logging.info("New ruleset contains %s rules" % len(rule_models))
    if (make_default):
        logging.info("New ruleset is now default")

    return True


def create_ruleset(*args, **kwargs):
    return mining_api.create_ruleset(*args, **kwargs)


def designate_default(ruleset_model):
    """
    Flag a ruleset as default - mark all others as not default
    TODO: Add a index for more efficient search
    TODO: This should leverage models (?)
    """
    ruleset_entity = mining_api._populate_ruleset_entity(ruleset_model)

    entities_to_update = []
    ruleset_models, cursor, more = mining_api._query_ruleset_entities()
    for m in ruleset_models:
        if m.is_default:
            m.is_default = False
            entities_to_update.append(m)

    # Update the new one
    ruleset_entity.is_default = True
    entities_to_update.append(ruleset_entity)  # Note: potential to overrite?

    if (entities_to_update):
        ndb.put_multi(entities_to_update)
        # mining_api.update_rulesets(entities_to_update)

    # Refresh the
    return mining_api._populate_ruleset_model(ruleset_entity)
