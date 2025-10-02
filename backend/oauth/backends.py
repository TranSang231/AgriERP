from oauth2_provider.backends import OAuth2Backend
from oauth2_provider.oauth2_backends import get_oauthlib_core
from django.core.exceptions import SuspiciousOperation

OAuthLibCore = get_oauthlib_core()


# Todo: Handle login for external authentication providers
# Reference: https://docs.djangoproject.com/en/5.0/topics/auth/customizing/
class CustomOAuth2Backend(OAuth2Backend):
    """
    Authenticate against an OAuth2 access token
    """

    def authenticate(self, request=None, **credentials):
        if request is not None:
            try:
                valid, request = OAuthLibCore.verify_request(request, scopes=[])
            except ValueError as error:
                if str(error) == "Invalid hex encoding in query string.":
                    raise SuspiciousOperation(error)
                else:
                    raise
            else:
                if valid:
                    return request.user

        return None