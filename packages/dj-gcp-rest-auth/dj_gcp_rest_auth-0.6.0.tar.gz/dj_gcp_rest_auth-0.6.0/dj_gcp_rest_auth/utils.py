"""Utility function for module
"""
import re
from typing import Optional, Dict

# Import libraries for token verification
from google.auth.transport.requests import Request
from google.oauth2 import id_token

from .settings import api_settings


def validate_gcp_token(gcp_token: Optional[str]) -> Optional[Dict[str, str]]:
    """[summary]

    :param gcp_token: Token to validate
    :type gcp_token: str
    :return: Payload if valid, None if not valid.
    :rtype: Optional[Dict[str, str]]
    """
    if not gcp_token:
        return None

    try:
        payload = id_token.verify_token(gcp_token, request=Request())
        for allowed_service_account_pattern in api_settings.ALLOWED_SERVICE_ACCOUNTS:
            if re.findall(allowed_service_account_pattern, payload['email']):
                return payload
    except ValueError:
        return None
    return None
