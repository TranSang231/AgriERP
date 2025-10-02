import django.conf


class OTPPhoneSettings:
    """
    This is a simple class to take the place of the global settings object.

    An instance will contain all of our settings as attributes, with default
    values if they are not specified by the configuration.

    """

    defaults = {
        'OTP_SMS_BODY_TEMPLATE_PATH': 'otp/phone/sms_message.html',
        'OTP_PHONE_TOKEN_VALIDITY': 600,
        'OTP_PHONE_THROTTLE_FACTOR': 1,
        'OTP_PHONE_COOLDOWN_DURATION': 60,
    }

    def __getattr__(self, name):
        if name in self.defaults:
            return getattr(django.conf.settings, name, self.defaults[name])
        else:
            return getattr(django.conf.settings, name)


settings = OTPPhoneSettings()
