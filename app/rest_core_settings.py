REST_DEFAULT_ORIGIN = 'https://pref-service-dev.appspot.com'  # TODO: Set at runtime re: ENV
REST_WHITELIST_DOMAINS = []

REST_WHITELIST_RULES = [r'http.*//pref-service-.*.appspot.com',
                        r'htt.*://divining-admin.appspot.com',
                        r'http://localhost:.*']

REST_MIDDLEWARE_CLASSES = [u'auth_core.middleware.AuthenticationMiddleware', ]
