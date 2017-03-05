"""
Preference Service
"""

from api import preference_api
from api import mining_api


def record_preference(preference_models):
    """"
    Method to persist a preference or list of preferences
    """

    is_single = False
    if not isinstance(preference_models, list):
        is_single = True
        preference_models = [preference_models]

    # Iterate over all the persistance models and convert to ndb models
    preference_models = preference_api.create_multi(preference_models)

    if (is_single):
        return preference_models[0]
    return preference_models


def generate_association_rules(min_support, min_confidence):
    """
    Process to generate association rules
    """
    # TODO: This probably needs to be split up into separate async functions

    txn_data = preference_api.get_txn_data()
    _, rule_models = mining_api.run_apriori(txn_data, min_support, min_confidence)
    rule_models = mining_api.create_rules(rule_models)

    return rule_models


def query_preferences(*args, **kwargs):
    """
    Query for a set of preferences - mostly used for debugging

    TODO: This is currently returning ndb models from the api
    """

    return preference_api.query_preference_entities(*args, **kwargs)
    # TODO: THIS NEEDS UNIT TESTS, ETC

