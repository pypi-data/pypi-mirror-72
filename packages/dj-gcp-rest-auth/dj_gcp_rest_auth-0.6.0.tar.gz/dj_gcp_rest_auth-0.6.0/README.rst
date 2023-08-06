===========================
Django GCP REST Auth
===========================


.. image:: https://img.shields.io/pypi/v/dj_gcp_rest_auth.svg
        :target: https://pypi.python.org/pypi/dj_gcp_rest_auth

.. image:: https://img.shields.io/gitlab/pipeline/pennatus/dj_gcp_rest_auth/master
        :alt: Gitlab pipeline status

.. image:: https://readthedocs.org/projects/dj_gcp_rest_auth/badge/?version=latest
        :target: https://dj_gcp_rest_auth.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


Provides a way to determine if an incoming request is coming from a GCP service account that
you have authorized.  You can also use this module to as a way of wrapping an identity token
which on its own has no access claims.  The wrapped token is an authenticated GCP token and
the inner token specifies the Django user.

For instance, an authenticated user requests an ``identity token`` using the ``/identity/`` endpoint.
This token on its own can not be used to access services.  The user then gives this identity token
to an IoT device that can obtain its own GCP Token.  When the IoT device wants to make a request on behalf
of the authenticated user, it adds the X-GCP-IDTOKEN header.

In another example, you may be using Google Functions from a pub/sub model to make a request to an API
endpoint on your Django server.  In this case your Google Function will have a default service
account and you can obtain an id-token within your Google Function.  An id-token is a JWT token
that contains various claims.  You will need to get an id-token that contains the email claim.
You can pass this token into your request using the Authorization header.  This module can then be
used to verify the token and make sure that the identity of the user belongs a list of
allowed service accounts that you configure.

* Free software: MIT license
* Documentation: https://dj_gcp_rest_auth.readthedocs.io.

Installation
------------

Install ``dj_gcp_rest_auth`` from pip ::

    $ pip install dj_gcp_rest_auth

Update your top level ``settings.py`` ::

    GCP_REST_AUTH = {
        'IDENTITY_TOKEN_LIFETIME_DAYS': 7,
        'ALLOWED_SERVICE_ACCOUNTS': ['11111122222-compute@developer.gserviceaccount.com']
    }

``IDENTITY_TOKEN_LIFETIME_DAYS`` is optional and if specified specify the lifetime of an identity token in days.
Identity tokens can be generated from this package.

``ALLOWED_SERVICE_ACCOUNTS`` is a list of regex patterns representing the service account emails that
are allowed to use your API.

In your views, set ::

    from dj_gcp_rest_auth.authentication import GCPTokenAuthentication

    class MyView(GenericAPIView):
        authentication_classes = ( GCPTokenAuthentication, )

Optionally, in your urls.py, set ::

    import dj_gcp_rest_auth

    path('', include(dj_gcp_rest_auth.urls))

Optionally, you can use the IsGCPUser custom permission.  This permission is useful to indicate that the
GCP Token is valid and from an authorized service account.

    from dj_gcp_rest_auth.permissions import IsGCPUser


Obtaining an id-token
---------------------

There are several ways to obtain an ``id-token`` from your Google service (Compute, GAE, Cloud Run, Function, etc.).

The following method only depends on ``curl`` and makes use of the internal meta data to retrieve the ``id-token`` ::

    curl -H "Metadata-Flavor: Google" "http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/identity?audience=arbitrary&format=full"


Authorization
-------------

Once you obtain an ``id-token``, your GCP service can authenticate with Django by passing your ``id-token``
with the ``Authorization`` header as shown in the following request ::

    curl -H "X-GCP-IDTOKEN: <user-id-token>" -H "Authorization: Bearer <my-id-token>" http://localhost:8000/protected/resource

The ``user-id-token`` is obtained from the ``/identity/`` endpoint.


Endpoints
---------

This package can be used to expose an endpoint to generate an identity token for the authenticated user ::

    GET /identity
