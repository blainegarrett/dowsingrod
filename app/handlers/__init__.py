import webapp2


class IndexHandler(webapp2.RequestHandler):
    """
    Base Handler for Non-api calls
    """

    def get(self):
        self.response.write("Suggest endpoint")
