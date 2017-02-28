"""
Preference Service
"""

from api import preference_api


def record_preference(preference_models):
    """"
    Method to persist a preference or list of preferences
    """

    if not isinstance(preference_models, list):
        preference_models = [preference_models]

    # Iterate over all the persistance models and convert to ndb models
    return preference_api.create_multi(preference_models)
