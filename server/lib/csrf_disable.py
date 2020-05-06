# -*- coding: utf-8 -*-

from rest_framework.authentication import SessionAuthentication


class CsrfExemptSessionAuthentication(SessionAuthentication):
    """Disable CSRF check in drf."""

    def enforce_csrf(self, request):
        """Disable CSRF check."""
        return  # noqa: WPS324
