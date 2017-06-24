""" Put all your allowed auth services here
This should be redesigned to be more generic.
However, if you need to implement SAML, Google Login, etc
    simply put your file here, and imlement
    user, login = get_user_by_token(token)

    When the authentication handler receives {auth_type: ..., auth_token: ...}
    The auth_type should resolve to the name of this file and the auth_token you can use to
    validate against your service.

    For example, in Google Auth Flow, the web client prompts the user to login, and upon successful login
    you will want to call your authentication endpoint with {auth_type: 'google', auth_token: <token_from_google>}

    Then you'd call out to google's service in your service helper and validate the token using your credentials
    Once google validates the call, you'd get our create a user and return it.

    From there, we use our own JWT authentication headers until they expire, etc.

    Also, note currently the Authentication: Basic <base64_encode_un:pw> dips into the basic service,
        but otherwise your primary means of external authentication needs to be through the authentication
        handler not the Auth headers.

    More documentation to come.

"""