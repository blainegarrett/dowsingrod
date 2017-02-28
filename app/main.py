"""
Main entry point
"""

import webapp2
from webapp2_extras.routes import RedirectRoute

import logging
import os
import sys

# Add the external libs
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'thirdparty'))


def handle_404(request, response, exception):

    # Generic 404 handler
    logging.exception(exception)

    response.write("Not found")
    response.set_status(404)

# Define routes - currently this is only the written RSS feed
web_routes = [
    RedirectRoute('/api/rest/suggest',
                  'handlers.rest.suggest.SuggestionHandler',
                  strict_slash=True,
                  name="index")]

app = webapp2.WSGIApplication(web_routes, debug=True)
app.error_handlers[404] = handle_404
