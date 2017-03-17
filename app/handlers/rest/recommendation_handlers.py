import voluptuous
from rest_core import handlers
from rest_core.resources import Resource
from rest_core.resources import RestField
from rest_core.resources import ResourceIdField
from rest_core.resources import ResourceUrlField

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
    ResourceIdField(output_only=True),
    ResourceUrlField('/api/rest/v1.0/recommendations/%s', output_only=True),
    RestField(AssociationRuleModel.ant, required=False),
    RestField(AssociationRuleModel.con, required=False),
    RestField(AssociationRuleModel.confidence, required=True),
    RestField(AssociationRuleModel.rule_key, output_only=True),
]

resource_url = '/api/rest/v1.0/rulesets/%s'
ASSOCIATION_RULE_SET_FIELDS = [
    ResourceIdField(output_only=True),
    ResourceUrlField('/api/rest/v1.0/recommendation/%s', output_only=True),
    RestField(AssociationRuleSetModel.min_confidence, output_only=True),
    RestField(AssociationRuleSetModel.min_support, output_only=True),
    RestField(AssociationRuleSetModel.total_rules, output_only=True),
    DatetimeField(AssociationRuleSetModel.created_timestamp, output_only=True),
]


class RuleSetHandler(handlers.RestHandlerBase):
    """
    Base Handler for Non-api calls
    """

    def get_rules(self):
        return []

    def model_to_rest_resource(self, model, verbose=False):
        """Convert a AssociationRuleModel to a Rest Resource (dict)"""
        return Resource(model, ASSOCIATION_RULE_SET_FIELDS).to_dict(verbose)


class RuleSetCollectionHandler(RuleSetHandler):

    def get_param_schema(self):
        # Validators for schema

        return {
            # 'pretty': voluptuous.Coerce(bool),   # TODO: Force rest api core to add this
            'min_confidence': voluptuous.Coerce(float),
            'min_support': voluptuous.Coerce(float)
        }

    def post(self):
        """
        Generate Rules
        TODO: Make this an async process
        """
        min_support = self.cleaned_params.get('min_support', DEFAULT_MIN_SUPPORT)
        min_confidence = self.cleaned_params.get('min_confidence', DEFAULT_MIN_CONFIDENCE)

        # Generate Ruleset
        ruleset_model = rule_service.create_ruleset(min_support, min_confidence)

        # Generate the rules for the set
        rule_service.generate_association_rules(ruleset_model.id, min_support, min_confidence)

        # Return the ruleset
        self.serve_success(self.model_to_rest_resource(ruleset_model, True))

    def get(self):
        # TODO: MOVE TO API LEVEL

        return_resources = []
        models = rule_service.query_rule_sets()
        for model in models:
            return_resources.append(self.model_to_rest_resource(model, True))
        self.serve_success(return_resources)


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

    def get(self):
        """
        Retrieve a set of rules based on the latest generated AssociationRuleSet
        """
        ruleset = rule_service.query_rule_sets()[0]
        models = rule_service.query_rules(ruleset_id=ruleset.id)
        return_resources = []
        for model in models:
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
