import json
from jwcrypto import jwt
from jwcrypto.common import JWException
from jwcrypto.jwt import JWTExpired
from oauth2_provider.oauth2_validators import OAuth2Validator
from .tokens import JWTAccessToken
from django.contrib.auth import get_user_model

from oauth2_provider.models import (
    get_access_token_model,
    get_id_token_model,
)
IDToken = get_id_token_model()
AccessToken = get_access_token_model()
User = get_user_model()

class CustomOAuth2Validator(OAuth2Validator):
    def validate_bearer_token(self, token, scopes, request):
        if self.validate_bearer_jwt_token(token, scopes, request):
            return True
        return super().validate_bearer_token(token, scopes, request)
    
    def validate_id_token(self, token, scopes, request):
        """
        When users try to access resources, check that provided id_token is valid
        """
        if not token:
            return False

        id_token = self._load_id_token(token)
        if not id_token:
            return False

        if not id_token.allow_scopes(scopes):
            return False
        
        request.client = id_token.application
        request.user = id_token.user
        request.scopes = scopes
        # this is needed by django rest framework
        request.access_token = id_token
        return True

    def _load_id_token(self, token):
        try:
            key = self._get_key_for_token(token)
        except Exception:
            # Malformed or non-JWS token
            return None
        if not key:
            return None
        try:
            jwt_token = jwt.JWT(key=key, jwt=token)
            claims = json.loads(jwt_token.claims)
            jti = claims.get("jti")
            if jti is None:
                return JWTAccessToken(claims)
            return IDToken.objects.get(jti=jti)
        except (JWException, JWTExpired, IDToken.DoesNotExist) as e:
            print(e)
            return None

    # Set `oidc_claim_scope = None` to ignore scopes that limit which claims to return,
    # otherwise the OIDC standard scopes are used.

    def get_additional_claims(self, request):
        return {
            "first_name": request.user.first_name,
            "last_name": request.user.last_name,
            "full_name": ' '.join([request.user.first_name, request.user.last_name]),
            "email": request.user.email,
        }
    
    # If we use jwt token for accesstoken
    def validate_bearer_jwt_token(self, token, scopes, request):
        try:
            key = self._get_key_for_token(token)
        except Exception:
            # Invalid JWS/JWT format or unsupported representation
            return False
        if not key:
            return False

        try:
            jwt_token = jwt.JWT(key=key, jwt=token)
            claims = json.loads(jwt_token.claims)
            jti = claims.get("jti")
            if jti is None:
                access_token = JWTAccessToken(claims)
                if access_token.is_valid(scopes):
                    request.client = access_token.application
                    request.user = access_token.user
                    request.scopes = list(access_token.scopes)
                    request.access_token = access_token
                    return True
        except Exception:
            return False

    def validate_user(self, username, password, client, request, *args, **kwargs):
        """
        Override to handle user validation properly.
        The parent class checks u.is_active, but when using JWT, it might create
        a JWTUser object that doesn't have is_active attribute.
        """
        try:
            u = User.objects.get(email=username)
        except User.DoesNotExist:
            return False
        
        if u is not None and u.is_active and u.check_password(password):
            request.user = u
            return True
        return False