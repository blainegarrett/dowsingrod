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


def query_rule_sets():
    return mining_api.query_ruleset_models()


def delete_rules():
    """
    Delete Rules
    TODO: May simply want to flag them as not the current set
    """
    return mining_api.delete_rules()


def generate_association_rules_async(ruleset_id, min_support, min_confidence):
    logging.info("Enqueuing generate_association_rules")
    async = Async(target='services.rule_service.generate_association_rules_async',
                  args=(ruleset_id, min_support, min_confidence))
    async.start()


def generate_association_rules(ruleset_id, min_support, min_confidence):
    """
    Process to generate association rules
    """
    # TODO: This probably needs to be split up into separate async functions
    # TODO: It feels weird importing the pref_api, but we need the prefs in our specific format
    log_args = (ruleset_id, min_support, min_confidence)
    logging.info("Starting Generation of Ruleset Completed with id %s - %s - %s " % log_args)

    txn_data = preference_api.get_txn_data()

    # TODO: Create an association_rule entity

    ruleset_model, rule_models = mining_api.run_apriori(txn_data, min_support, min_confidence)
    rule_models = mining_api.create_rules(ruleset_id, rule_models)

    # Update rule model with total count
    ruleset_model = mining_api.get_ruleset_by_id(ruleset_id)

    # TODO: THIS SHOULD HAPPEN in the api layer
    e = mining_api._populate_ruleset_entity(ruleset_model)
    e.total_rules = len(rule_models)
    e.put()

    logging.info("Completing generation of Ruleset Completed with id %s - %s - %s " % log_args)
    logging.info("New ruleset contains %s rules" % len(rule_models))

    return True


def create_ruleset(*args, **kwargs):
    return mining_api.create_ruleset(*args, **kwargs)
