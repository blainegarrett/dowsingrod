"""
Preference Service
"""

from api import preference_api
from api import mining_api


def record_preference(preference_models):
    """"
    Method to persist a preference or list of preferences
    """

    if not isinstance(preference_models, list):
        preference_models = [preference_models]

    # Iterate over all the persistance models and convert to ndb models
    return preference_api.create_multi(preference_models)


def generate_association_rules(min_support, min_confidence):
    """
    Process to generate association rules
    """
    # TODO: This probably needs to be split up into separate async functions

    txn_data = preference_api.get_txn_data()
    _, rule_models = mining_api.run_apriori(txn_data, min_support, min_confidence)
    rule_models = mining_api.create_rules(rule_models)

    return rule_models
