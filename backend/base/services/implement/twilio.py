import phonenumbers
from django.conf import settings
from django.utils import translation
from django.utils.translation import pgettext
from twilio.rest import Client

# Supported voice languages
VOICE_LANGUAGES = ('en', 'en-gb', 'es', 'fr', 'it', 'de', 'da-DK', 'de-DE',
                   'en-AU', 'en-CA', 'en-GB', 'en-IN', 'en-US', 'ca-ES',
                   'es-ES', 'es-MX', 'fi-FI', 'fr-CA', 'fr-FR', 'it-IT',
                   'ja-JP', 'ko-KR', 'nb-NO', 'nl-NL', 'pl-PL', 'pt-BR',
                   'pt-PT', 'ru-RU', 'sv-SE', 'zh-CN', 'zh-HK', 'zh-TW')


class Twilio:
    """
    Gateway for sending text messages and making phone calls using Twilio_.

    All you need is your Twilio Account SID and Token, as shown in your Twilio
    account dashboard.

    ``TWILIO_ACCOUNT_SID``
      Should be set to your account's SID.

    ``TWILIO_AUTH_TOKEN``
      Should be set to your account's authorization token.

    ``TWILIO_CALLER_ID``
      Should be set to a verified phone number. Twilio_ differentiates between
      numbers verified for making phone calls and sending text messages.

    ``TWILIO_MESSAGING_SERVICE_SID``
      Can be set to a Twilio Messaging Service for SMS. This service can wrap multiple
      phone numbers and choose one depending on the destination country.
      When left empty the ``TWILIO_CALLER_ID`` will be used as sender ID.

    .. _Twilio: http://www.twilio.com/
    """

    def __init__(self):
        self.client = Client(getattr(settings, 'TWILIO_ACCOUNT_SID'),
                             getattr(settings, 'TWILIO_AUTH_TOKEN'))
        
    def to_e164(self, phone, region=None):
        """
        return phone number in the E.164 format
        [+][code pays][phone number with area code]
        0901111111 => +84901111111
        """
        try:
            if region:
                region = region.upper()
            _phone = phonenumbers.parse(phone, region=region)
            phone = phonenumbers.format_number(
                _phone, phonenumbers.PhoneNumberFormat.E164
            )
        except phonenumbers.NumberParseException:
            return None
        return phone

    def make_call(self, number, content_uri):
        locale = translation.get_language()
        validate_voice_locale(locale)
        self.client.calls.create(to=self.to_e164(number),
                                 from_=getattr(settings, 'TWILIO_CALLER_ID'),
                                 url=content_uri, method='GET', timeout=15)

    def send_sms(self, number, content):
        """
        send the content to the phone number via sms 
        """
        send_kwargs = {
            'to': self.to_e164(number),
            'body': content
        }
        messaging_service_sid = getattr(settings, 'TWILIO_MESSAGING_SERVICE_SID', None)
        if messaging_service_sid is not None:
            send_kwargs['messaging_service_sid'] = messaging_service_sid
        else:
            send_kwargs['from_'] = getattr(settings, 'TWILIO_CALLER_ID')

        self.client.messages.create(**send_kwargs)


def validate_voice_locale(locale):
    with translation.override(locale):
        voice_locale = pgettext('twilio_locale', 'en')
        if voice_locale not in VOICE_LANGUAGES:
            raise NotImplementedError('The language "%s" is not '
                                      'supported by Twilio' % voice_locale)
