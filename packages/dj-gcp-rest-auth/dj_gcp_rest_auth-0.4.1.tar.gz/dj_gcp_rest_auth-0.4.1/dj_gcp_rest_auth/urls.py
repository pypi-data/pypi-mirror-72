"""URLs exported by this module.
"""
from django.urls import path

from .views import TokenObtainIdentityView

urlpatterns = [
    # URLs that do not require a session or valid token
    path('identity/', TokenObtainIdentityView.as_view(), name='token_obtain_identity'),
]
