# Handlers for Transaction Sets

import voluptuous

from rest_core.resources import Resource
from rest_core.resources import RestField
from rest_core.resources import DatetimeField
from rest_core.resources import ResourceUrlField
from rest_core.resources import ResourceIdField
from rest_core.exc import DoesNotExistException
from auth_core.decorators import authentication_required

from handlers.rest import BaseRestHandler
from services import transaction_service
from models import TransactionModel

resource_url = '/api/rest/v1.0/transactions/%s'
TRANSACTION_FIELDS = [
    ResourceIdField(output_only=True, verbose_only=True),
    ResourceUrlField(resource_url, output_only=True, verbose_only=True),
    RestField(TransactionModel.rule_item_ids, output_only=True),
    RestField(TransactionModel.total_preferences, output_only=True),
    RestField(TransactionModel.total_dislikes, output_only=True),
    RestField(TransactionModel.total_likes, output_only=True),
    RestField(TransactionModel.user_id, output_only=True),
    DatetimeField(TransactionModel.created_timestamp, output_only=True),
    DatetimeField(TransactionModel.latest_timestamp, output_only=True),
]


class TransactionBaseHandler(BaseRestHandler):
    """
    Base Handler for Preferences
    """

    def get_rules(self):
        return TRANSACTION_FIELDS

    def get_model_by_id_or_error(self, resource_id):
        """
        Fetch a model by given id OR implicitly raise a 404
        """

        m = transaction_service.get_by_id(resource_id)

        if not m:
            err = 'Preference with resource_id \'%s\' not found'
            raise DoesNotExistException(err % resource_id)
        return m

    def model_to_rest_resource(self, model, verbose=False):
        """Convert a PreferenceModel to a Rest Resource (dict)"""
        return Resource(model, TRANSACTION_FIELDS).to_dict(verbose)


class TransactionDetailHandler(TransactionBaseHandler):
    """
    Handler for a single Preference
    """
    # TODO: Update this to operate off of user_id

    @authentication_required
    def get(self, resource_id):
        pref_model = self.get_model_by_id_or_error(resource_id)
        result = self.model_to_rest_resource(pref_model,
                                             self.cleaned_params.get('verbose'))
        self.serve_success(result)


class TransactionCollectionHandler(TransactionBaseHandler):
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
        models, next_cursor, more = transaction_service.query(**kwargs)
        return_resources = []
        for pref_model in models:
            return_resources.append(self.model_to_rest_resource(pref_model, is_verbose))
        self.serve_success(return_resources, {'cursor': next_cursor, 'more': more})
