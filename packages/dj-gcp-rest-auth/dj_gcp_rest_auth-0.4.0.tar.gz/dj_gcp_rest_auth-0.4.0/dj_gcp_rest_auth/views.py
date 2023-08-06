"""Views exported by the module.
"""

from rest_framework import (
    generics,
    status,
    response,
    permissions,
)
from .serializers import TokenObtainIdentitySerializer


class TokenObtainIdentityView(generics.GenericAPIView):
    """Used to obtain a JWT Token that is simply used to prove identity.
    It has no access or refresh rights.
    """
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = TokenObtainIdentitySerializer

    def post(self, request, *_args, **_kwargs):
        """This is the POST implementation for obtaining an identity token.

        Simply returns back a new identity token for the authenticated user.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return response.Response(serializer.data, status=status.HTTP_200_OK)
