import voluptuous

from rest_core.resources import Resource
from rest_core.resources import RestField
from rest_core.resources import DatetimeField
from rest_core.resources import ResourceUrlField
from rest_core.resources import ResourceIdField
from rest_core.exc import DoesNotExistException
from auth_core.decorators import authentication_required

from handlers.rest import BaseRestHandler
from services import item_service
from models import ItemModel

resource_url = '/api/rest/v1.0/items/%s'
ITEM_FIELDS = [
    ResourceIdField(output_only=True, verbose_only=True),
    ResourceUrlField(resource_url, output_only=True, verbose_only=True),
    RestField(ItemModel.item_id, required=True),
    RestField(ItemModel.total_preferences, required=True),
    RestField(ItemModel.total_dislikes, required=True),
    RestField(ItemModel.total_likes, required=True),
    DatetimeField(ItemModel.created_timestamp, output_only=True),
    DatetimeField(ItemModel.latest_timestamp, output_only=True),
]


class ItemBaseHandler(BaseRestHandler):
    """
    Base Handler for Preferences
    """

    def get_rules(self):
        return ITEM_FIELDS

    def get_model_by_id_or_error(self, resource_id):
        """
        Fetch a model by given id OR implicitly raise a 404
        """

        m = item_service.get_by_id(resource_id)

        if not m:
            err = 'Preference with resource_id \'%s\' not found'
            raise DoesNotExistException(err % resource_id)
        return m

    def model_to_rest_resource(self, model, verbose=False):
        """Convert a PreferenceModel to a Rest Resource (dict)"""
        return Resource(model, ITEM_FIELDS).to_dict(verbose)


class ItemDetailHandler(ItemBaseHandler):
    """
    Handler for a single Preference
    """
    @authentication_required
    def get(self, resource_id):
        pref_model = self.get_model_by_id_or_error(resource_id)
        result = self.model_to_rest_resource(pref_model,
                                             self.cleaned_params.get('verbose'))
        self.serve_success(result)


class ItemCollectionHandler(ItemBaseHandler):
    """
    Handler for a collection of Preferences
    """

    def get_param_schema(self):
        return {
            u'limit': voluptuous.Coerce(int),
            u'cursor': voluptuous.Coerce(str),
            u'item_ids': voluptuous.Coerce(str)
        }

    @authentication_required
    def get(self):
        kwargs = {
            'limit': self.cleaned_params.get('limit', None),
            'cursor': self.cleaned_params.get('cursor', None)
        }

        item_id_str = self.cleaned_params.get('item_ids', None)
        is_verbose = self.cleaned_params.get('verbose')
        return_resources = []

        # They're fetching by an list of items
        if (item_id_str):
            item_ids = item_id_str.split(',')
            models = item_service.get_by_item_ids(item_ids)
            next_cursor = None
            more = False
        else:
            models, next_cursor, more = item_service.query(**kwargs)

        for pref_model in models:
            return_resources.append(self.model_to_rest_resource(pref_model, is_verbose))
        self.serve_success(return_resources, {'cursor': next_cursor, 'more': more})
