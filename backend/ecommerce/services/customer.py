from base.services import BaseService, Mailing, Verification
from django.conf import settings
from django.contrib.auth.hashers import check_password
from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomerService(BaseService):

    @classmethod
    def send_customer_verify_email(
        cls,
        email,
        first_name,
        last_name,
        frontend_host,
        user_id=None,
        customer_id=None,
    ):
        data= {
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "frontend_host": frontend_host
        }
        if user_id is not None:
            data.update({"user_id": user_id})
        if customer_id is not None:
            data.update({"customer_id": customer_id})
        token = Verification.create_token(data=data)
        scheme = (
            "http"
            if frontend_host.startswith("localhost") or frontend_host.startswith("127.0.0.1")
            else "https"
        )
        link = f"{scheme}://{frontend_host}/customers/verify?token={token}"
        default_host = settings.DEFAULT_HOST
        default_scheme = (
            "http"
            if default_host.startswith("localhost") or default_host.startswith("127.0.0.1")
            else "https"
        )
        logo = f"{default_scheme}://{default_host}/static/logo.jpg"
        data = {
            "template": "ecommerce/emails/verify_customer_email.html",
            "subject": _("Verify your Alpha Shop account"),
            "context": {
                "email": email,
                "first_name": first_name,
                "last_name": last_name,
                "token": token,
                "link": link,
                "logo": logo,
                "lang": "en" #Todo make it dynamic
            },
            "to": [email],
        }
        message = Mailing.create_html_message(data=data)
        Mailing.asyn_send_message(message=message)

    @classmethod
    def send_forgot_password_email(cls, email, frontend_host, language="en"):
        try:
            user = User.objects.filter(email=email).first() # Sử dụng mô hình User
            if not user:
                    raise ValueError(_("The email does not exist."))

            if not user.is_active:
                raise ValueError(_("The account were not activated."))

            data = {"email": email}
            token = Verification.create_token(data=data)

            scheme = (
                "http"
                if frontend_host.startswith("localhost") or frontend_host.startswith("127.0.0.1")
                else "https"
            )
            link = f"{scheme}://{frontend_host}/reset_password?token={token}"
            
            default_host = settings.DEFAULT_HOST
            default_scheme = (
                "http"
                if default_host.startswith("localhost") or default_host.startswith("127.0.0.1")
                else "https"
            )
            logo = f"{default_scheme}://{default_host}/static/logo.svg"
            data = {
                "template": "ecommerce/emails/forgot_password_email.html",
                "subject": _("Password Reset Request"),
                "context": {
                    "email": email,
                    "link": link,
                    "logo": logo,
                    "lang": language
                },
                "to": [email],
            }
            
            message = Mailing.create_html_message(data=data)
            Mailing.asyn_send_message(message=message)
        except ValueError as ve:
            print(ve)
            raise ValueError(ve)

        except Exception as e:
            print(e)
            raise ValueError(_("An error occurred."))

    @classmethod
    def set_password(cls, token, new_password):
        try:
            data = Verification.verify_token(token)
            email = data.get("email")

            user = User.objects.filter(email=email).first()
            if not user:
                raise ValueError(_("User not found."))

            if not user.is_active:
                raise ValueError(_("The account were not activated."))

            user.set_password(new_password)
            user.save()
        except Verification.TokenExpiredError:
            raise ValueError(_("Token has expired."))
        except Verification.TokenInvalidError:
            raise ValueError(_("Invalid token."))
        except Exception as e:
            print(e)
            raise ValueError(_("An error occurred."))
        

    @classmethod
    def change_password(cls, email, current_password, new_password):
        try:
            user = User.objects.filter(email=email).first()
            if not user:
                raise ValueError(_("User not found."))

            if not user.is_active:
                raise ValueError(_("The account were not activated."))

            if not check_password(current_password, user.password):
                raise ValueError(_("Current password is incorrect."))

            user.set_password(new_password)
            user.save()
        except ValueError as ve:
            raise ValueError(ve)
        except Exception as e:
            print(e)
            raise ValueError(_("An error occurred."))
