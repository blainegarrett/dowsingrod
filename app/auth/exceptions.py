class AuthenticationError(Exception):
    """
    Base Authentication Error class

    These are caught when a user attempts to authenticate.
    The exception is caught in the middleware and more generic RESt 401 is thrown
    This means you can put descriptive messages in the Exception w/o worrying it
    will bubble up to the end user.
    """

    pass
