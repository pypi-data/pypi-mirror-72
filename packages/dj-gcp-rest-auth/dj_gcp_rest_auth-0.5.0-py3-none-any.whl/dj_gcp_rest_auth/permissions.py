"""Permissions exported by package
"""

from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import View

from .utils import validate_gcp_token


class IsGCPUser(BasePermission):
    """Is the request coming from a valid GCP user.
    """
    def has_permission(self, request: Request, view: View) -> bool:
        """Returns whether request is coming from a valid GCP user.
        """
        return validate_gcp_token(request.auth)
