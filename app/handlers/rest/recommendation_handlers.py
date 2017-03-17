import voluptuous
from rest_core import handlers
from rest_core.resources import Resource
from rest_core.resources import RestField
from rest_core.resources import ResourceIdField
from rest_core.resources import ResourceUrlField

from models import PreferenceModel
from models import AssociationRuleModel
from services import rule_service
from services import preference_service
from handlers.rest import dataset


# Default Support and Confidence
DEFAULT_MIN_SUPPORT = .75
DEFAULT_MIN_CONFIDENCE = .5

resource_url = '/api/rest/v1.0/recommendation/%s'
ASSOCIATION_RULES_FIELDS = [
    ResourceIdField(output_only=True),
    ResourceUrlField(resource_url, output_only=False),
    RestField(AssociationRuleModel.ant, required=False),
    RestField(AssociationRuleModel.con, required=False),
    RestField(AssociationRuleModel.confidence, required=True),
    RestField(AssociationRuleModel.rule_key, output_only=True),
]


class RecommendationsHandler(handlers.RestHandlerBase):
    """
    Base Handler for Non-api calls
    """
    def get_rules(self):
        return ASSOCIATION_RULES_FIELDS

    def model_to_rest_resource(self, model, verbose=False):
        """Convert a AssociationRuleModel to a Rest Resource (dict)"""
        return Resource(model, ASSOCIATION_RULES_FIELDS).to_dict(verbose)


class RecommendationCollectionHandler(RecommendationsHandler):
    """
    """

    def get(self):  # TODO: Switch to post or put
        """
        Retrieve a set of rules
        """
        models = rule_service.query_rules()
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

    def post(self):
        """
        Generate Rules
        """
        min_support = self.cleaned_params.get('min_support', DEFAULT_MIN_SUPPORT)
        min_confidence = self.cleaned_params.get('min_confidence', DEFAULT_MIN_CONFIDENCE)

        models = preference_service.generate_association_rules(min_confidence, min_support)
        return_resources = []
        for model in models:
            return_resources.append(self.model_to_rest_resource(model, True))
        self.serve_success(return_resources)

    def delete(self):
        """
        Clear out the stale association rules
        TODO: Return a list of keys of the deleted items?
        """
        rule_service.delete_rules()
        self.serve_success([])
