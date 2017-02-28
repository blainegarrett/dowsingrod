
import webapp2


class BaseHandler(webapp2.RequestHandler):
    """
    Base Handler for Non-api calls
    """


class IndexHandler(webapp2.RequestHandler):
    """
    Base Handler for Non-api calls
    """

    def get(self):
        self.response.write("Welcome to the Dowsing Rod project")
