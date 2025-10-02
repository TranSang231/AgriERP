from rest_framework_api_key.models import BaseAPIKeyManager


class ApiKeyManager(BaseAPIKeyManager):
    def get_api_key(self, key: str) -> bool:
        api_key = None
        try:
            api_key = self.get_from_key(key)
        except self.model.DoesNotExist:
            return None

        if api_key.has_expired:
            return None

        return api_key
