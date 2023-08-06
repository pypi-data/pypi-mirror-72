"""JWT Tokens exported
"""
from datetime import timedelta
from rest_framework_simplejwt.tokens import Token
from django.contrib.auth import get_user_model

from .settings import api_settings


class IdentityToken(Token):
    """JWT Token with just the identity claim.  Used to indicate a specific user.
      The 'user' claim will contain the Django User Id
    """
    token_type = 'identity'
    lifetime = timedelta(days=api_settings.IDENTITY_TOKEN_LIFETIME_DAYS)

    def __init__(self, *args, user_id=None) -> None:
        super().__init__(*args)
        if user_id:
            self['user'] = user_id

    def get_user(self):
        """Returns the Django user represented by the user_id specified in
           the user claim.
        """
        return get_user_model().objects.get(pk=self['user'])

    def verify_token_type(self):
        """
        Untyped tokens do not verify the "token_type" claim.  This is useful
        when performing general validation of a token's signature and other
        properties which do not relate to the token's intended use.
        """
