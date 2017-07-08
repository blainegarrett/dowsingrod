import voluptuous

from rest_core.resources import Resource
from rest_core.resources import RestField
from rest_core.resources import BooleanField
from rest_core.resources import DatetimeField
from rest_core.resources import ResourceUrlField
from rest_core.resources import ResourceIdField
from rest_core.exc import DoesNotExistException
from auth.decorators import authentication_required

from handlers.rest import BaseRestHandler
from services import preference_service
from models import PreferenceModel

resource_url = '/api/rest/v1.0/preferences/%s'
PREFERENCE_FIELDS = [
    ResourceIdField(output_only=True, verbose_only=True),
    ResourceUrlField(resource_url, output_only=True, verbose_only=True),
    RestField(PreferenceModel.user_id, required=True),
    RestField(PreferenceModel.item_id, required=True),
    BooleanField(PreferenceModel.pref, required=True),
    DatetimeField(PreferenceModel.timestamp, required=False),
    DatetimeField(PreferenceModel.synced_timestamp, output_only=True),
]


class PreferenceBaseHandler(BaseRestHandler):
    """
    Base Handler for Preferences
    """

    def get_rules(self):
        return PREFERENCE_FIELDS

    def get_model_by_id_or_error(self, resource_id):
        """
        Fetch a model by given id OR implicitly raise a 404
        """

        m = preference_service.get_by_id(resource_id)

        if not m:
            err = 'Preference with resource_id \'%s\' not found'
            raise DoesNotExistException(err % resource_id)
        return m

    def model_to_rest_resource(self, model, verbose=False):
        """Convert a PreferenceModel to a Rest Resource (dict)"""
        return Resource(model, PREFERENCE_FIELDS).to_dict(verbose)


class PreferenceDetailHandler(PreferenceBaseHandler):
    """
    Handler for a single Preference
    """
    @authentication_required
    def get(self, resource_id):
        pref_model = self.get_model_by_id_or_error(resource_id)
        result = self.model_to_rest_resource(pref_model,
                                             self.cleaned_params.get('verbose'))
        self.serve_success(result)


class PreferenceCollectionHandler(PreferenceBaseHandler):
    """
    Handler for a collection of Preferences
    """

    def get_param_schema(self):
        return {
            u'limit': voluptuous.Coerce(int),
            u'cursor': voluptuous.Coerce(str),
        }

    @authentication_required
    def get(self):
        kwargs = {
            'limit': self.cleaned_params.get('limit', None),
            'cursor': self.cleaned_params.get('cursor', None)
        }

        is_verbose = self.cleaned_params.get('verbose')
        models, next_cursor, more = preference_service.query_preferences(**kwargs)
        return_resources = []
        for pref_model in models:
            return_resources.append(self.model_to_rest_resource(pref_model, is_verbose))
        self.serve_success(return_resources, {'cursor': next_cursor, 'more': more})

    def validate_payload(self):  # aka Form.clean
        """
        Validate the request payload against the rest rules
        """

        # This is easy to screw up for this handler and the err is otherwise confusing
        if not isinstance(self.data, list):
            t = type(self.data)
            raise Exception("Expecting a `list` of Preference Resources. Received %s" % t)

        self.cleaned_data = []
        for d in self.data:
            self.cleaned_data.append(Resource(None, PREFERENCE_FIELDS).from_dict(d))

    @authentication_required
    def post(self):
        models = []
        return_resources = []
        is_verbose = self.cleaned_params.get('verbose')
        for d in self.cleaned_data:
            model = PreferenceModel(d.get('user_id'),
                                    d.get('item_id'),
                                    d.get('pref'),
                                    d.get('timestamp'))
            models.append(model)

        models = preference_service.record_preference(models)
        for pref_model in models:
            return_resources.append(self.model_to_rest_resource(pref_model, is_verbose))
        self.serve_success(return_resources)
