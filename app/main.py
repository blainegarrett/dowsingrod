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

# Define routes - currently this is only the written RSS feed
web_routes = [
    RedirectRoute('/api/rest/v1.0/recommendations',
                  'handlers.rest.recommendation_handlers.RecommendationsHandler',
                  strict_slash=True,
                  name="RecommendationsHandler"),
    RedirectRoute('/api/rest/v1.0/preferences/list',
                  'handlers.rest.preference_handlers.PreferenceListHandler',
                  strict_slash=True,
                  name="PreferenceCollectionHandler"),
    RedirectRoute('/api/rest/v1.0/preferences/<resource_id:\w+>',
                  'handlers.rest.preference_handlers.PreferenceDetailHandler',
                  strict_slash=True,
                  name="PreferenceDetailHandler"),
    RedirectRoute('/api/rest/v1.0/preferences',
                  'handlers.rest.preference_handlers.PreferenceCollectionHandler',
                  strict_slash=True,
                  name="PreferenceCollectionHandler"),
    ]
app = webapp2.WSGIApplication(web_routes, debug=True)
app.error_handlers[404] = handle_404
