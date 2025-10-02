from django.contrib.humanize.templatetags.humanize import naturaltime
from django.db import models
from django.template.loader import render_to_string
from django.utils.translation import gettext
from base.services import SMS

from .base import (
    CooldownMixin,
    GenerateNotAllowed,
    SideChannelDevice,
    ThrottlingMixin,
    TimestampMixin,
)
from ..util import hex_validator, random_hex

from ..settings.phone import settings


def default_key():  # pragma: no cover
    """Obsolete code here for migrations."""
    return random_hex(20)


def key_validator(value):  # pragma: no cover
    """Obsolete code here for migrations."""
    return hex_validator()(value)


class PhoneOTPDevice(TimestampMixin, CooldownMixin, ThrottlingMixin, SideChannelDevice):
    """
    A :class:`~django_otp.models.SideChannelDevice` that delivers a token to
    the email address saved in this object or alternatively to the user's
    registered email address (``user.email``).

    The tokens are valid for :setting:`OTP_PHONE_TOKEN_VALIDITY` seconds. Once
    a token has been accepted, it is no longer valid.

    Note that if you allow users to reset their passwords by email, this may
    provide little additional account security. It may still be useful for,
    e.g., requiring the user to re-verify their email address on new devices.

    .. attribute:: email

        *EmailField*: An alternative email address to send the tokens to.

    """

    phone = models.CharField(
        max_length=15,
        blank=True,
        unique=True,
        help_text='Optional alternative phone number to send tokens to',
    )

    def generate_challenge(self, extra_context=None):
        """
        Generates a random token and emails it to the user.

        :param extra_context: Additional context variables for rendering the
            email template.
        :type extra_context: dict

        """
        generate_allowed, data_dict = self.generate_is_allowed()
        if generate_allowed:
            message = self._deliver_token(extra_context)
        else:
            if data_dict['reason'] == GenerateNotAllowed.COOLDOWN_DURATION_PENDING:
                next_generation_naturaltime = naturaltime(
                    data_dict['next_generation_at']
                )
                message = (
                    "Token generation cooldown period has not expired yet. Next"
                    f" generation allowed {next_generation_naturaltime}."
                )
            else:
                message = "Token generation is not allowed at this time"
        print(message)
        return message

    def _deliver_token(self, extra_context):
        self.cooldown_set(commit=False)
        self.generate_token(valid_secs=settings.OTP_PHONE_TOKEN_VALIDITY, commit=True)

        context = {'token': self.token, **(extra_context or {})}
        body = render_to_string(
            settings.OTP_SMS_BODY_TEMPLATE_PATH,
            {'token': self.token}
        )

        self.send_sms(body, **(extra_context or {}))

        message = gettext("sent by sms")

        return message
    
    def send_sms(self, body, **kwargs):
        message = {
            **kwargs,
            'to': self.phone,
            'content': body
        }
        SMS.asyn_send_message(message)

    def verify_token(self, token):
        """"""
        verify_allowed, _ = self.verify_is_allowed()
        if verify_allowed:
            verified = super().verify_token(token)

            if verified:
                self.throttle_reset(commit=False)
                self.set_last_used_timestamp(commit=False)
                self.save()
            else:
                self.throttle_increment()
        else:
            verified = False

        return verified

    def get_cooldown_duration(self):
        """
        Returns :setting:`OTP_PHONE_COOLDOWN_DURATION`.
        """
        return settings.OTP_PHONE_COOLDOWN_DURATION

    def get_throttle_factor(self):
        """
        Returns :setting:`OTP_PHONE_THROTTLE_FACTOR`.
        """
        return settings.OTP_PHONE_THROTTLE_FACTOR
