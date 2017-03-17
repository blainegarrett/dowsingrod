from api import mining_api


def query_rules():
    """
    TODO: Support filters, paginations, etc
    """
    return mining_api.query_rule_models()


def delete_rules():
    """
    Delete Rules
    TODO: May simply want to flag them as not the current set
    """
    return mining_api.delete_rules()
