"""
Simple Decorators for Auth System
"""
from rest_core.errors import PermissionException
from auth_settings import REQUIRE_AUTHENTICATION


def authentication_required(handler_method):
    """
    Simple decorator to apply to rest method functions to require an authenticated user
    """
    def ensure_authenticated(self, *args, **kwargs):
        if REQUIRE_AUTHENTICATION:
            user = getattr(self.request, '_user', None)  # TODO: Replace with auth helper
            if not (user and user.is_authenticated()):
                raise PermissionException("Authentication Required")
        return handler_method(self, *args, **kwargs)

    return ensure_authenticated
