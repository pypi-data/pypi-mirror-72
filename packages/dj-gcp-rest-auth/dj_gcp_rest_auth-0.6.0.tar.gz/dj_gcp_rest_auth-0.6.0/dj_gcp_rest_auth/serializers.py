"""Serializers exported by the module.
"""
from rest_framework.request import Request
from rest_framework import serializers

from .tokens import IdentityToken


class TokenObtainIdentitySerializer(serializers.Serializer):
    """Used to get a JWT token with the user claim set to the pk of the authenticated user
    """
    identity = serializers.SerializerMethodField(required=False)

    def get_identity(self, *_args, **_kwargs):
        """Returns the identity token
        """
        request: Request = self.context['request']
        return str(IdentityToken(user_id=request.user.pk))

    def create(self, *_args, **_kwargs):
        """Unused
        """

    def update(self, *_args, **_kwargs):
        """Unused
        """
