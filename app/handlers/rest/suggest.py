import webapp2


class SuggestionHandler(webapp2.RequestHandler):
    """
    Base Handler for Non-api calls
    """

    def get(self):

        # Snag the session_id
        session_id = self.request.GET('session_id', None)

        # See if they have a session, otherwise make a best guess

        #


class RecordPreference(webapp2.RequestHandler):
    """
    Record a single preference
    """

    def get(self):  # TODO: Switch to post or put
        session_id = self.request.GET('session_id', None)  # session
        item_id = self.request.GET('item_id', None)  # artwork, gallery, etc
        pref = self.request.GET('pref', None)  # like or dislike
        timestamp = self.request.GET('timestamp', None)  # like or dislike

        # Construct a preference Model
        p = PreferenceModel(session_id, item_id, pref, timestamp=timestamp)

        # service.record_preference(p)





        raise Exception(session_id)
        self.response.write("Suggest endpoint")

"""
- Endpoints
- record pref
- record pref bulk


"""
