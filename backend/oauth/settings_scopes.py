from oauth2_provider.settings import oauth2_settings
from oauth2_provider.scopes import BaseScopes
from oauthlib.oauth2.rfc6749.utils import scope_to_list

from oauth2_provider.models import (
    get_access_token_model,
    get_application_model,
    get_id_token_model,
)

Application = get_application_model()
AccessToken = get_access_token_model()
IDToken = get_id_token_model()


class SettingsScopes(BaseScopes):
    def get_all_scopes(self):
        return oauth2_settings.SCOPES

    def get_available_scopes(self, application=None, request=None, *args, **kwargs):
        all_scopes = set(oauth2_settings._SCOPES)
        #Todo: retrict non-system applications' scopes

        if application is not None:
            application_scopes = all_scopes if  application.scope == '__all__' else set(scope_to_list(application.scope))
            # validate application scopes
            return list(application_scopes.intersection(all_scopes))
        return list(all_scopes)

    def get_default_scopes(self, application=None, request=None, *args, **kwargs):
        return oauth2_settings._DEFAULT_SCOPES