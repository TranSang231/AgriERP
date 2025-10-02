from datetime import datetime

import jwt
from django.conf import settings
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext as _

from .base import BaseService


class Verification(BaseService):
    # Định nghĩa một thuộc tính cho TokenExpiredError ngay trong lớp Verification
    TokenExpiredError = type('TokenExpiredError', (Exception,), {})
    TokenInvalidError = type('TokenInvalidError', (Exception,), {})

    @staticmethod
    def get_header():
        return {"alg": "HS256", "typ": "JWT"}

    @staticmethod
    def get_secret_key():
        return settings.SECRET_KEY

    @staticmethod
    def create_token(data, life_time=3600):
        if not isinstance(data, dict):
            raise ValidationError(detail=_("Invalid format"))
        
        payload = data
        payload.update({
            "iat": datetime.now().timestamp(),
            "exp": datetime.now().timestamp() + life_time
        })

        token = jwt.encode(payload, Verification.get_secret_key(), algorithm="HS256")
        return token

    @staticmethod
    def decode_token(token):
        payload = jwt.decode(token, Verification.get_secret_key(), algorithms=["HS256"])
        if 'iat' in payload:
            del payload['iat']
        
        if 'exp' in payload:
            exp = int(payload.get("exp"))
            if datetime.now().timestamp() > exp:
                raise Verification.TokenExpiredError(_('Token expired!'))
            del payload['exp']
        return payload

    
    @staticmethod
    def verify_token(token):
        try:
            payload = Verification.decode_token(token)
            # Token is valid
            return payload
        except Verification.TokenExpiredError as e:
            # Handle token expired case
            raise Verification.TokenExpiredError(_('Token expired!'))
        except Verification.TokenInvalidError as e:
            # Handle invalid token case
            raise Verification.TokenInvalidError(_('Invalid token!'))