"""Authentication schemes exported by module
"""
from django.contrib.auth.models import AnonymousUser

from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.authentication import JWTAuthentication

from .tokens import IdentityToken
from .utils import validate_gcp_token


class GCPTokenAuthentication(JWTAuthentication):
    """Use to make sure the request contains a GCP verified JWT token.

       The JWT token must contain the email claim and the email must be in
       the list of ALLOWED_SERVICE_ACCOUNTS in your settings.
    """
    def authenticate(self, request):
        """Perform authentication and return the user in the audience.
        """
        header = self.get_header(request)
        if not header:
            return None

        gcp_token = self.get_raw_token(header)

        # If the request doesn't contain a GCP token then it is definitely not from a GCP user.
        if not gcp_token:
            return None

        payload = validate_gcp_token(gcp_token)
        if not payload:
            return None

        try:
            token = IdentityToken(payload['aud'])
            return token.get_user(), gcp_token
        except TokenError:
            return AnonymousUser(), gcp_token
