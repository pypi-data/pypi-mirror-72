"""Settings specific to the dj_gcp_rest_auth module
"""
from typing import Dict, List, Union
from django.conf import settings
from django.test.signals import setting_changed
from rest_framework.settings import APISettings


USER_SETTINGS = getattr(settings, 'GCP_REST_AUTH', None)

DEFAULTS: Dict[str, Union[None, str, List[str]]] = {
    'IDENTITY_TOKEN_LIFETIME_DAYS': 7, # Days the identity token is valid for.
                                       # This token does not have the access or refresh claim
                                       # so it can't be used to access resources.
    'ALLOWED_SERVICE_ACCOUNTS': [],
}

IMPORT_STRINGS = (
)

REMOVED_SETTINGS = (
)


#pylint: disable=invalid-name
api_settings = APISettings(USER_SETTINGS, DEFAULTS, IMPORT_STRINGS)


def reload_api_settings(*_args, **kwargs):
    """Signal handler for handling automatic reloading of settings.
    """
    #pylint: disable=global-statement
    global api_settings

    setting, value = kwargs['setting'], kwargs['value']

    if setting == 'GCP_REST_AUTH':
        api_settings = APISettings(value, DEFAULTS, IMPORT_STRINGS)


setting_changed.connect(reload_api_settings)
