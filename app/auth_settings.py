"""
Settings for Auth System
"""

# Temp setting to lockdown handler methods using auth.decorators.authentication_required
REQUIRE_AUTHENTICATION = True

# These should be environment specific
JWT_SECRET = 'lucretia'
JWT_ISSUER = 'https://localhost:9090'  # This doesn't need to be a specific value, but is validated
JWT_AUDIENCE = 'preference-engine'  # This doesn't need to be a specific value, but is validated
JWT_EXPIRATION = 60*60
