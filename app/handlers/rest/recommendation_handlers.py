import voluptuous
import itertools
import logging
from rest_core import handlers
from rest_core.resources import Resource
from rest_core.resources import RestField
from rest_core.resources import ResourceIdField
from rest_core.resources import ResourceUrlField
from rest_core.resources import BooleanField

from rest_core.resources import DatetimeField

from models import PreferenceModel
from models import AssociationRuleModel
from models import AssociationRuleSetModel

from services import rule_service
from services import preference_service
from handlers.rest import dataset


# Default Support and Confidence
DEFAULT_MIN_SUPPORT = .75
DEFAULT_MIN_CONFIDENCE = .5

ASSOCIATION_RULES_FIELDS = [
    ResourceIdField(output_only=True, verbose_only=True),
    ResourceUrlField('/api/rest/v1.0/recommendations/%s', output_only=True,  verbose_only=True),
    RestField(AssociationRuleModel.ant, required=False),
    RestField(AssociationRuleModel.con, required=False),
    RestField(AssociationRuleModel.confidence, required=True),
    RestField(AssociationRuleModel.rule_key, output_only=True),
]

resource_url = '/api/rest/v1.0/rulesets/%s'
ASSOCIATION_RULE_SET_FIELDS = [
    ResourceIdField(output_only=True, verbose_only=True),
    ResourceUrlField('/api/rest/v1.0/rulesets/%s', output_only=True,  verbose_only=True),
    RestField(AssociationRuleSetModel.min_confidence, output_only=True),
    RestField(AssociationRuleSetModel.min_support, output_only=True),
    RestField(AssociationRuleSetModel.total_rules, output_only=True),
    BooleanField(AssociationRuleSetModel.is_default, output_only=True),
    DatetimeField(AssociationRuleSetModel.created_timestamp, output_only=True, verbose_only=True),
]


def generate_rule_key(ant):
    """
    Generate an identifier for a rule key based on the antecedant items
    """

    # General cleanup
    cleaned_items = []
    for item in ant:
        cleaned_items.append(item.lower().replace(' ', '_'))

    # Sort
    cleaned_items.sort()

    # Concat them together
    return '__'.join(cleaned_items)


class RuleSetHandler(handlers.RestHandlerBase):
    """
    Base Handler for Non-api calls
    """

    def get_rules(self):
        return []

    def model_to_rest_resource(self, model, verbose=False):
        """Convert a AssociationRuleModel to a Rest Resource (dict)"""
        return Resource(model, ASSOCIATION_RULE_SET_FIELDS).to_dict(verbose)


class RuleSetDetailHandler(RuleSetHandler):
    def get(self, ruleset_id):
        """
        Fetch a ruleset by id
        """
        model = rule_service.get_rule_set(ruleset_id)
        resource = self.model_to_rest_resource(model, True)
        self.serve_success(resource)

    def put(self, ruleset_id):
        # Make an association ruleset default
        model = rule_service.get_rule_set(ruleset_id)
        if not model:
            raise Exception("Ruleset does not exist")

        model = rule_service.designate_default(model)
        resource = self.model_to_rest_resource(model, True)
        self.serve_success(resource)


class RuleSetCollectionHandler(RuleSetHandler):

    def get_param_schema(self):
        # Validators for schema

        return {
            u'min_confidence': voluptuous.Coerce(float),
            u'min_support': voluptuous.Coerce(float),
            u'make_default': voluptuous.Coerce(voluptuous.Boolean()),
            u'limit': voluptuous.Coerce(int),
            u'cursor': voluptuous.Coerce(str),
        }

    def post(self):
        """
        Generate Rules
        """
        make_default = self.cleaned_params.get('make_default', False)
        min_support = self.cleaned_params.get('min_support', DEFAULT_MIN_SUPPORT)
        min_confidence = self.cleaned_params.get('min_confidence', DEFAULT_MIN_CONFIDENCE)

        # Generate Ruleset
        ruleset_model = rule_service.create_ruleset(min_support, min_confidence)

        # Generate the rules for the set
        rule_service.generate_association_rules_async(ruleset_model.id, min_support,
                                                      min_confidence, make_default)

        # Return the ruleset
        self.serve_success(self.model_to_rest_resource(ruleset_model,
                                                       self.cleaned_params.get('verbose')))

    def get(self):
        # Return a paginated list of association rule sets
        return_resources = []
        is_verbose = self.cleaned_params.get('verbose')

        kwargs = {
            'limit': self.cleaned_params.get('limit', None),
            'cursor': self.cleaned_params.get('cursor', None)
        }
        models, next_cursor, more = rule_service.query_rule_sets(**kwargs)
        for model in models:
            return_resources.append(self.model_to_rest_resource(model, is_verbose))
        self.serve_success(return_resources, {'cursor': next_cursor, 'more': more})


# Association Rules
class RecommendationsHandlerBase(handlers.RestHandlerBase):
    """
    Base Handler for Non-api calls
    """
    def get_rules(self):
        return ASSOCIATION_RULES_FIELDS

    def model_to_rest_resource(self, model, verbose=False):
        """Convert a AssociationRuleModel to a Rest Resource (dict)"""
        return Resource(model, ASSOCIATION_RULES_FIELDS).to_dict(verbose)


class RecommendationCollectionHandler(RecommendationsHandlerBase):
    """
    """

    def get_param_schema(self):
        # Validators for schema

        return {
            u'ruleset_id': voluptuous.Coerce(str),
            u'limit': voluptuous.Coerce(int),
            u'cursor': voluptuous.Coerce(str),
        }

    def get(self):
        """
        Retrieve a set of rules based on a generated AssociationRuleSet
        """

        # Determine AssociationRuleSet to use
        if self.cleaned_params.get('ruleset_id', None):
            ruleset_id = self.cleaned_params['ruleset_id']
        else:
            # TODO: None check... return default rules?
            rulessets, cursor, more = rule_service.query_rule_sets()
            if len(rulessets) == 0:
                raise Exception("There are no rulesets generated. TODO: smart defaults?")

            # TODO: Adding an index on is_default might be more scalable here
            ruleset_id = rulessets[0].id  # default to latest
            for r in rulessets:
                if r.is_default:
                    ruleset_id = r.id
                    break

        # Query for the rule models by ruleset_id
        kwargs = {
            'ruleset_id': ruleset_id,
            'limit': self.cleaned_params.get('limit', None),
            'cursor': self.cleaned_params.get('cursor', None)
        }

        models, next_cursor, more = rule_service.query_rules(**kwargs)
        return_resources = []
        for model in models:
            return_resources.append(self.model_to_rest_resource(model, True))
        self.serve_success(return_resources, {'cursor': next_cursor, 'more': more})


class RecommendationForUserHandler(RecommendationsHandlerBase):
    """
    Handler to get a recco for a specific user
    """

    def get_reccomendations_for_user(self, user_id):

        # Get Preferences for the user
        pref_models, cursor, more = preference_service.query_preferences(user_id=user_id)
        if (not pref_models):
            logging.error('no prefs for user... revert to defaults')
            return []

        # TODO: We're ignoring cursor, and more here for now. See: /issues/9

        # Generate a set of keys for these items to be used in rule look ups
        pref_key_list = {}
        for p in pref_models:
            pref_key_list[p.get_rule_item_id()] = p

        # Generate all the combos
        combos = []
        for r in range(len(pref_key_list)):
            combos += list(itertools.combinations(pref_key_list, r + 1))

        # Convert the combos to keys to do look up on rules
        rule_keys = []
        for c in combos:
            rule_keys.append(generate_rule_key(c))

        # Query for all the assoc rules
        # Determine AssociationRuleSet to use
        rules = rule_service.query_rule_sets()
        if len(rules) == 0:
            return []
            logging.error("There are no rulesets generated. TODO: smart defaults?")
        ruleset_id = rules[0].id

        # Query for the rule models by ruleset_id
        rule_models = rule_service.query_rules(ruleset_id=ruleset_id)

        rule_map = {}
        for rule_model in rule_models:
            rule_map[rule_model.rule_key] = rule_model

        return_rule_models = []
        # See if any of our keys match rules that we have not seen yet
        for rule_key in rule_keys:
            rule = rule_map.get(rule_key)

            if (rule):
                potential_target_id = rule.con[0].split(':')[0]

                # Figure out if we have not pref'd it yet
                target_not_seen = True
                for item_key, p in pref_key_list.items():

                    if potential_target_id == p.item_id:
                        target_not_seen = False
                if target_not_seen:
                    return_rule_models.append(rule)

        if not return_rule_models:
            logging.error("No association rules exist...")
        return return_rule_models

    def get_param_schema(self):
        # Validators for schema

        return {
            'ruleset_id': voluptuous.Coerce(str),
        }

    def get(self, user_id):
        """
        Retrieve a set of rules based on a generated AssociationRuleSet
        """

        return_resources = []
        for model in self.get_reccomendations_for_user(user_id):
            return_resources.append(self.model_to_rest_resource(model, True))
        self.serve_success(return_resources)


class SyncHandler(handlers.RestHandlerBase):

    def get_param_schema(self):
        # Validators for schema

        return {
            # 'pretty': voluptuous.Coerce(bool),   # TODO: Force rest api core to add this
            'min_confidence': voluptuous.Coerce(float),
            'min_support': voluptuous.Coerce(float)
        }

    def get_rules(self):
        return []

    def model_to_rest_resource(self, model, verbose=False):
        """Convert a AssociationRuleModel to a Rest Resource (dict)"""
        return Resource(model, ASSOCIATION_RULES_FIELDS).to_dict(verbose)

    def put(self):
        """ Temp debug bit to generate Preference data"""
        raise Exception('This is disbled')
        u = 0
        models_to_put = []
        for txn in dataset.data2:
            u += 1
            for txn_item in txn:
                models_to_put.append(PreferenceModel("user%s" % u, txn_item, True))
        preference_service.record_preference(models_to_put)
        self.serve_success('now run a POST')

    def delete(self):
        """
        Clear out the stale association rules
        TODO: Return a list of keys of the deleted items?
        """
        rule_service.delete_rules()
        self.serve_success([])
