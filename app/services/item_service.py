from api import item_api


def get_by_item_ids(item_ids):
    """
    Fetch a list of Item Models by their item_id
    TODO: Sort by total_preferences reverse
    """

    return item_api.get_by_item_ids(item_ids)


def query(*args, **kwargs):
    return item_api.query(*args, **kwargs)


def update_item(preference_models):
    """
    Update the item histograms
    """
    # TODO: Eventually do this in a async task based on preference resource_ids?

    # Step 1: Construct a mapping of item -> list of pref data tuples
    item_map = {}
    for preference_model in preference_models:
        if (not item_map.get(preference_model.item_id)):
            item_map[preference_model.item_id] = []

        # Append this preference tuple
        item_map[preference_model.item_id].append((preference_model.user_id,
                                                   preference_model.item_id,
                                                   preference_model.pref))

    # Finally update the items for each preference
    for item_id, pref_data in item_map.items():
        item_api.create_or_update_multi(item_id, pref_data)
    return
