"""Authentication schemes exported by module
"""
import re

# Import libraries for token verification
from google.auth.transport.requests import Request
from google.oauth2 import id_token

from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed

from .settings import api_settings
from .tokens import IdentityToken


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
            raise AuthenticationFailed("No token provided")

        gcp_token = self.get_raw_token(header)

        # If the request doesn't contain a GCP token then it is definitely not from a GCP user.
        if not gcp_token:
            raise AuthenticationFailed("No token provided")

        try:
            payload = id_token.verify_token(gcp_token, request=Request())
            for allowed_service_account_pattern in api_settings.ALLOWED_SERVICE_ACCOUNTS:
                if re.findall(allowed_service_account_pattern, payload['email']):
                    try:
                        token = IdentityToken(payload['aud'])
                        return token.get_user(), token
                    except TokenError:
                        return None
            raise AuthenticationFailed("Service account does not haver permission")
        except ValueError:
            raise AuthenticationFailed("Invalid token specified or token expired")
