
from api import transaction_api


def query(*args, **kwargs):
    return transaction_api.query(*args, **kwargs)


def update_transaction(preference_models):
    """
    """
    # TODO: Eventually do this in a async task
    # Step 1: Construct a mapping of user -> list of pref data tuples
    user_map = {}
    for preference_model in preference_models:
        if (not user_map.get(preference_model.user_id)):
            user_map[preference_model.user_id] = []

        # Append this preference tuple
        user_map[preference_model.user_id].append((preference_model.user_id,
                                                   preference_model.item_id,
                                                   preference_model.pref))

    # Finally update the items for each preference
    for user_id, pref_data in user_map.items():
        transaction_api.create_or_update_multi(user_id, pref_data)
    return
