import json
from django.http import HttpResponse
from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_406_NOT_ACCEPTABLE,
    HTTP_500_INTERNAL_SERVER_ERROR
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from drf_nested_forms.utils import NestedForm
from oauthlib.oauth2.rfc6749.utils import list_to_scope
from oauth2_provider.views.mixins import OAuthLibMixin
from oauth2_provider.signals import app_authorized
from oauth2_provider.models import get_access_token_model
from django.contrib.auth import get_user_model
from common.constants import Http
from core.settings.base import (
    BUSINESS_CLIENT_ID,
    BUSINESS_CLIENT_SECRET,
)
from base.views.base import BaseViewSet
from base.services import Verification
from oauth.serializers import UserShortSerializer
from oauth.permissions import IsAdministrator
from ..models import Employee
from ..serializers import EmployeeSerializer
from ..services import EmployeeService

User = get_user_model()
AccessToken = get_access_token_model()

class EmployeeViewSet(OAuthLibMixin, BaseViewSet):
    queryset = Employee.objects.exclude(roles__name__in=["Super Administrator"])
    serializer_class = EmployeeSerializer
    search_map = {
        "first_name": "icontains",
        "last_name": "icontains",
        "work_mail": "icontains"
    }
    required_alternate_scopes = {
        "create": [["admin:employees:edit"], ["employees:edit"]],
        "update": [["admin:employees:edit"], ["employees:view"]],
        "destroy": [["admin:employees:edit"], ["employees:edit"]],
        "invite": [["admin:employees:edit"], ["employees:edit"]],
        "list": [["admin:employees:view"], ["employees:view"]],
        "retrieve": [["admin:employees:view"], ["employees:view"]]
    }

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        origin = request.META.get("HTTP_ORIGIN")
        content_type = request.content_type
        if content_type is not None and 'form-data' in content_type:
            form = NestedForm(request.data)
            if form.is_nested():
                data = form.data

        email = data.get("work_mail")
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        user = data.get("user", None)
        # only create user after they verify their email
        if user is not None:
            del data['user']
        try:
            user_id = User.objects.get(email=email).id.urn[9:]
        except User.DoesNotExist:
            user_id = None
        
        serializer = self.get_serializer(data=data)
        if serializer.is_valid(raise_exception=True):
            self.perform_create(serializer)
            self.clear_querysets_cache()
            try:
                employee_id = serializer.data.get('id')
                EmployeeService.verify_employee_email(
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    employee_id=employee_id,
                    user_id=user_id,
                    origin=origin
                )
            except Exception as e:
                print(e)
                Response({"message": _("There is an error occur.")}, status=HTTP_500_INTERNAL_SERVER_ERROR)
            return Response(serializer.data, status=HTTP_201_CREATED)

    @action(detail=True, methods=[Http.HTTP_POST], url_path="invite")
    def invite(self, request, *args, **kwargs):
        instance = self.get_object()  
        email = instance.work_mail
        first_name = instance.first_name
        last_name = instance.last_name
        employee_id = instance.id.urn[9:]
        origin = request.META.get("HTTP_ORIGIN")

        try:
            user_id = User.objects.get(email=email).id.urn[9:]
        except User.DoesNotExist:
            user_id = None
        
        try:
            EmployeeService.verify_employee_email(
                email=email,
                first_name=first_name,
                last_name=last_name,
                employee_id=employee_id,
                user_id=user_id,
                origin=origin
            )
            Response({"message": _("The invitation have been sent.")}, status=HTTP_200_OK)
        except Exception as e:
            print(e)
            Response({"message": _("There is an error occur.")}, status=HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({"message": _("The invitation have been sent.")}, status=HTTP_200_OK)
    
    @action(detail=False, methods=[Http.HTTP_POST], url_path="verify", permission_classes=[AllowAny], authentication_classes=[])
    def verify(self, request, *args, **kwargs):
        content_type = request.content_type
        data = request.data.copy()
        if content_type is not None and 'form-data' in content_type:
            form = NestedForm(request.data)
            if form.is_nested():
                data = form.data
        
        employee_id = data.get('employee_id', None)
        if employee_id is None:
            return Response(
                {"error": _("Invalid employee id.")},
                status=HTTP_406_NOT_ACCEPTABLE
            )
        else:
            del data['employee_id']

        user_id = data.get('user_id', None)
        if user_id is not None:
            del data['user_id']

        token = data.get('token', None)
        if token is not None:
            del data['token']

        password = data.get('password')
        if password is not None:
            del data['password']
        email = data.get('email')

        try:
            # Check if the token were isssued to the right people
            token_payload = Verification.decode_token(token)
            token_email = token_payload.get('email')
            if email is not None and token_email != email:
                return Response(
                    {"error": _("Invalid token")},
                    status=HTTP_406_NOT_ACCEPTABLE
                )
        except Exception as e:
            print(e)
            return Response(
                {"error": _("Invalid token")},
                status=HTTP_406_NOT_ACCEPTABLE,
            )
        try:
            employee = Employee.objects.get(pk=employee_id)
            # user, created = User.objects.get_or_create(defaults=None,**data)
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                user = User.objects.create(**data)
            if user is not None and password is not None:
                user.set_password(password)
                user.save()

            if employee is not None and user is not None:
                employee.user = user
                employee.save()
        except Exception as e:
            print(e)
            return Response(
                {"error": _("User not found.")},
                status=HTTP_404_NOT_FOUND
            )
        return Response({"message": _("Verified")}, status=HTTP_200_OK)
    
    @action(detail=False, methods=[Http.HTTP_POST], url_path="login", permission_classes=[AllowAny], authentication_classes=[])
    def login(self, request, pk=None):
        try:
            user_name = request.POST.get("username")
            user = User.objects.prefetch_related("employees").get(email=user_name)
        except User.DoesNotExist:
            return Response(
                    {"error": _("The user does not exist.")},
                    status=HTTP_404_NOT_FOUND,
                )
        scopes = set()
        # Employee permissions
        if user.employees:
            employee = user.employees.first()
            if employee is not None:
                if employee.roles is not None:
                    for role in  employee.roles.all():
                        scopes = scopes.union(set(role.scopes.keys()))
           
        request.POST._mutable = True
        request.POST.update(
            {
                "grant_type": "password",
                "client_type": "confidential",
                "client_id": BUSINESS_CLIENT_ID,
                "client_secret": BUSINESS_CLIENT_SECRET
            }
        )
        if len(scopes) > 0:
            request.POST.update({"scope": list_to_scope(scopes)})

        url, headers, body, status = self.create_token_response(request)
        if status == 200:
            access_token = json.loads(body).get("access_token")
            if access_token is not None:
                token = AccessToken.objects.get(token=access_token)
                app_authorized.send(sender=self, request=request, token=token)
        response = HttpResponse(content=body, status=status)

        for k, v in headers.items():
            response[k] = v
        return response

    @action(detail=False, methods=[Http.HTTP_POST], url_path="refresh-token", permission_classes=[AllowAny], authentication_classes=[])
    def refeshToken(self, request):
        request.POST._mutable = True
        refresh_token =  request.POST.get("refresh_token")
        if not refresh_token or refresh_token == 'null':
            return Response(
                {"error": _("Invalid token")},
                status=HTTP_406_NOT_ACCEPTABLE,
            )
        request.POST.update(
            {
                "grant_type": "refresh_token",
                "client_id": BUSINESS_CLIENT_ID,
                "client_secret": BUSINESS_CLIENT_SECRET,
                "refresh_token": refresh_token,
            }
        )
        url, headers, body, status = self.create_token_response(request)
        if status == 200:
            access_token = json.loads(body).get("access_token")
            if access_token is not None:
                token =AccessToken.objects.get(token=access_token)
                app_authorized.send(sender=self, request=request, token=token)
        response = HttpResponse(content=body, status=status)

        for k, v in headers.items():
            response[k] = v
        return response

    @action(detail=False, methods=[Http.HTTP_POST], url_path="logout", permission_classes=[IsAuthenticated])
    def logout(self, request, pk=None):
        request.POST._mutable = True
        refresh_token = request.POST.get("refresh_token")
        access_token = request.POST.get("access_token")

        # revoke refresh_token first, to make user can not renew access_token
        request.POST.update(
            {
                "client_id": BUSINESS_CLIENT_ID,
                "client_secret": BUSINESS_CLIENT_SECRET,
                "token_type_hint": "refresh_token",
                "token": refresh_token,
            }
        )
        url, headers, body, status = self.create_revocation_response(request)
        if status != HTTP_200_OK:
            return Response(
                {"error": _("Can not revoke refresh token.")},
                status=HTTP_400_BAD_REQUEST,
            )

        # revoke access_token
        request.POST.update(
            {
                "token_type_hint": "access_token",
                "token": access_token,
            }
        )
        url, headers, body, status = self.create_revocation_response(request)
        if status != HTTP_200_OK:
            return Response(
                content={"error": _("Can not revoke access token.")},
                status=HTTP_400_BAD_REQUEST,
            )

        return Response({"message": _("Logout success!")}, status=HTTP_200_OK)
    
    @action(detail=False, methods=[Http.HTTP_POST], url_path="forgot_password", permission_classes=[AllowAny], authentication_classes=[])
    def forgot_password(self, request, *args, **kwargs):
        email = request.data.get("email")
        
        try:
            EmployeeService.send_forgot_password_email(email=email)
            return Response({"message": _("The link has been sent.")}, status=HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({"message": _("An error occurred.")}, status=HTTP_500_INTERNAL_SERVER_ERROR)
        
    
    
    
    @action(detail=False, methods=[Http.HTTP_POST], url_path="reset_password", permission_classes=[AllowAny], authentication_classes=[])
    def reset_password(self, request, *args, **kwargs):
        token = request.data.get("token")
        new_password = request.data.get("password")
        
        try:
            EmployeeService.set_password(token=token, new_password=new_password)
            return Response({"message": _("Password has been reset.")}, status=HTTP_200_OK)

        except ValueError as ve:
            return Response({"message": str(ve)}, status=HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(e)
            return Response({"message": _("An error occurred.")}, status=HTTP_500_INTERNAL_SERVER_ERROR)
        
            
    
    @action(detail=False, methods=["POST"], url_path="change-password", permission_classes=[AllowAny], authentication_classes=[])
    def change_password(self, request, *args, **kwargs):
        email = request.data.get("email")
        current_password = request.data.get("current_password")
        new_password = request.data.get("new_password")
        
        try:
            EmployeeService.change_password(email=email, current_password=current_password, new_password=new_password)
            return Response({"message": _("Password has been changed.")}, status=HTTP_200_OK)

        except ValueError as ve:
            return Response({"message": str(ve)}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(e)
            return Response({"message": _("An error occurred.")}, status=HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=[Http.HTTP_GET], url_path="userinfo", permission_classes=[IsAuthenticated])
    def userinfo(self, request, *args, **kwargs):
        try:
            id = request.auth.user.id
            user = get_object_or_404(User.objects.all(), id=id)
            user_serializer= UserShortSerializer(user)
            user_data = user_serializer.data
            return Response(user_data, status=HTTP_200_OK)
        except Exception as e:
            return Response({"message": _("Business not found.")}, status=HTTP_404_NOT_FOUND)

    @action(detail=False, methods=[Http.HTTP_GET], url_path="scopes", permission_classes=[IsAdministrator])
    def scopes(self, request, pk=None):
        from oauth2_provider.scopes import get_scopes_backend
        scopes_backend = get_scopes_backend()
        all_scopes = scopes_backend.get_all_scopes()
        default_scopes = scopes_backend.get_default_scopes()
        # scopes = {name: desc for name, desc in all_scopes.items() if name in business_scopes}
        # default_scopes = [name for name in default_scopes if name in business_scopes]
        
        return Response({ "scopes" :all_scopes, "default_scopes": default_scopes }, status=HTTP_200_OK)