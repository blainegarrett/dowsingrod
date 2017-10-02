"""
Main entry point
"""

import webapp2
from webapp2_extras.routes import RedirectRoute

import logging


def handle_404(request, response, exception):

    # Generic 404 handler
    logging.exception(exception)

    response.write("Not found")
    response.set_status(404)


# Define routes
web_routes = [
    RedirectRoute('/api/rest/v1.0/rulesets',
                  'handlers.rest.v1_0.recommendation_handlers.RuleSetCollectionHandler',
                  strict_slash=True,
                  name="RuleSetCollectionHandler"),

    RedirectRoute('/api/rest/v1.0/rulesets/<ruleset_id>',
                  'handlers.rest.v1_0.recommendation_handlers.RuleSetDetailHandler',
                  strict_slash=True,
                  name="RuleSetCollectionHandler"),


    RedirectRoute('/api/rest/v1.0/recommendations',
                  'handlers.rest.v1_0.recommendation_handlers.RecommendationCollectionHandler',
                  strict_slash=True,
                  name="RecommendationsHandler"),

    RedirectRoute('/api/rest/v1.0/recommendations/<user_id>',
                  'handlers.rest.v1_0.recommendation_handlers.RecommendationForUserHandler',
                  strict_slash=True,
                  name="RecommendationForUserHandler"),

    RedirectRoute('/api/rest/v1.0/preferences/list',
                  'handlers.rest.v1_0.preference_handlers.PreferenceListHandler',
                  strict_slash=True,
                  name="PreferenceCollectionHandler"),

    RedirectRoute('/api/rest/v1.0/preferences',
                  'handlers.rest.v1_0.preference_handlers.PreferenceCollectionHandler',
                  strict_slash=True,
                  name="PreferenceCollectionHandler"),

    RedirectRoute('/api/rest/v1.0/preferences/<resource_id:\w+>',
                  'handlers.rest.v1_0.preference_handlers.PreferenceDetailHandler',
                  strict_slash=True,
                  name="PreferenceDetailHandler"),

    RedirectRoute('/api/rest/v1.0/items',
                  'handlers.rest.v1_0.item_handlers.ItemCollectionHandler',
                  strict_slash=True,
                  name="ItemCollectionHandler"),

    # Not Implemented
    RedirectRoute('/api/rest/v1.0/items/<resource_id:\w+>',
                  'handlers.rest.v1_0.item_handlers.ItemDetailHandler',
                  strict_slash=True,
                  name="ItemDetailHandler"),

    RedirectRoute('/api/rest/v1.0/transactions',
                  'handlers.rest.v1_0.transaction_handlers.TransactionCollectionHandler',
                  strict_slash=True,
                  name="TransactionCollectionHandler"),

    # Not Implemented
    RedirectRoute('/api/rest/v1.0/transactions/<user_id:\w+>',
                  'handlers.rest.v1_0.transaction_handlers.TransactionDetailHandler',
                  strict_slash=True,
                  name="TransactionDetailHandler"),

    RedirectRoute('/api/rest/v1.0/sync',
                  'handlers.rest.v1_0.recommendation_handlers.SyncHandler',
                  strict_slash=True,
                  name="SyncHandler"),

    RedirectRoute('/api/auth/authenticate',
                  'auth.handlers.AuthenticationHandler',
                  strict_slash=True,
                  name="AuthenticationHandler"),

    RedirectRoute('/api/auth/users',
                  'auth.handlers.UsersCollectionHandler',
                  strict_slash=True,
                  name="UsersCollectionHandler"),

    RedirectRoute('/api/auth/users/<user_resource_id:\w+>',
                  'auth.handlers.UserResourceHandler',
                  strict_slash=True,
                  name="UserResourceHandler"),

    RedirectRoute('/api/auth/users/<user_resource_id:\w+>/logins',
                  'auth.handlers.UserLoginsCollectionHandler',
                  strict_slash=True,
                  name="UserLoginsCollectionHandler"),

    RedirectRoute('/api/auth/users/<user_resource_id:\w+>/logins/password',
                  'auth.handlers.UserLoginsPasswordHandler',
                  strict_slash=True,
                  name="UserLoginsPasswordHandler"),

    RedirectRoute('/api/auth/users/<user_resource_id:\w+>/logins/<login_resource_id:\w+>',
                  'auth.handlers.UserLoginsResourceHandler',
                  strict_slash=True,
                  name="UserLoginsResourceHandler"),

    ]
app = webapp2.WSGIApplication(web_routes, debug=True)
app.error_handlers[404] = handle_404
