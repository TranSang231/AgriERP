import json
from django.http import HttpResponse
from django.db import transaction
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND,
    HTTP_406_NOT_ACCEPTABLE,
    HTTP_500_INTERNAL_SERVER_ERROR
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import ValidationError
from drf_nested_forms.utils import NestedForm
from oauthlib.oauth2.rfc6749.utils import list_to_scope
from oauth2_provider.views.mixins import OAuthLibMixin
from oauth2_provider.signals import app_authorized
from oauth2_provider.models import get_access_token_model
from django.contrib.auth import get_user_model
from common.constants import Http
from oauth.constants import AccountStatus
from core.settings.base import (
    BUSINESS_CLIENT_ID,
    BUSINESS_CLIENT_SECRET,
    SECRET_KEY
)
from base.views.base import BaseViewSet
from base.services import Verification
from oauth.serializers import UserShortSerializer
from oauth.permissions import IsAdministrator
from ..models import Customer
from ..serializers import CustomerSerializer
from ..services import CustomerService

User = get_user_model()
AccessToken = get_access_token_model()

class CustomerViewSet(OAuthLibMixin, BaseViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    search_map = {
        "first_name": "icontains",
        "last_name": "icontains",
        "email": "icontains"
    }
    required_alternate_scopes = {
        "create": [["ecommerce:customers:edit"], ["ecommerce:customers:edit-mine"]],
        "update": [["ecommerce:customers:edit"], ["ecommerce:customers:edit-mine"]],
        "destroy": [["ecommerce:customers:edit"], ["ecommerce:customers:edit-mine"]],
        "register": [["admin:employees:edit"], ["employees:edit"]],
        "list": [["ecommerce:customers:view"], ["ecommerce:customers:edit"]],
        "retrieve": [
            ["ecommerce:customers:view"],
            ["ecommerce:customers:view-mine"],
            ["ecommerce:customers:edit"],
            ["ecommerce:customers:edit-mine"]
        ]
    }

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        content_type = request.content_type
        if content_type is not None and 'form-data' in content_type:
            form = NestedForm(request.data)
            if form.is_nested():
                data = form.data

        frontend_host = request.get_host()
        email = data.get("email")
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
                customer_id = serializer.data.get('id')
                CustomerService.send_customer_verify_email(
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    frontend_host=frontend_host,
                    user_id=user_id,
                    customer_id=customer_id
                )
            except Exception as e:
                print(e)
                Response({"message": _("There is an error occur.")}, status=HTTP_500_INTERNAL_SERVER_ERROR)
            return Response(serializer.data, status=HTTP_201_CREATED)
        
    @action(detail=False, methods=[Http.HTTP_POST], url_path="register", permission_classes=[AllowAny], authentication_classes=[])
    def register(self, request, *args, **kwargs):
        frontend_host = request.get_host()
        email = request.data.get("email")
        first_name = request.data.get("first_name")
        last_name = request.data.get("last_name")
        password = request.data.get("password")
        
        if not email or not password:
            return Response({"detail": "Email and password are required."}, status=HTTP_400_BAD_REQUEST)
        
        if len(password) < 6:
            return Response({"detail": "Password must be at least 6 characters."}, status=HTTP_400_BAD_REQUEST)
        
        # Check if customer already exists
        try:
            customer = Customer.objects.get(email=email)
            return Response({"detail": "A customer account with that email already exists."}, status=HTTP_400_BAD_REQUEST)
        except Customer.DoesNotExist:
            pass  # Customer doesn't exist, which is what we want
        
        try:
            with transaction.atomic():
                # Create user if not exists
                try:
                    user = User.objects.get(email=email)
                    return Response({"detail": "User with this email already exists."}, status=HTTP_400_BAD_REQUEST)
                except User.DoesNotExist:
                    user = User.objects.create_user(
                        email=email,
                        password=password,
                        first_name=first_name or "",
                        last_name=last_name or ""
                    )
                
                # Create customer
                customer = Customer.objects.create(
                    user=user,
                    email=email,
                    first_name=first_name or "",
                    last_name=last_name or "",
                    status=AccountStatus.ACTIVE
                )
                
                # Return simple success without token for now (to avoid OAuth complexity)
                customer_serializer = CustomerSerializer(customer)
                return Response({
                    "message": _("Registration successful! Please log in."),
                    "customer": customer_serializer.data
                }, status=HTTP_201_CREATED)
                    
        except Exception as e:
            import traceback
            print(f"Registration error: {e}")
            print(traceback.format_exc())
            return Response({"message": _("Registration failed. Please try again.")}, status=HTTP_500_INTERNAL_SERVER_ERROR)

    
    @action(detail=False, methods=[Http.HTTP_POST], url_path="verify", permission_classes=[AllowAny], authentication_classes=[])
    def verify(self, request, *args, **kwargs):
        content_type = request.content_type
        data = request.data.copy()
        if content_type is not None and 'form-data' in content_type:
            form = NestedForm(request.data)
            if form.is_nested():
                data = form.data
        
        customer_id = data.get('customer_id', None)
        if customer_id is not None:
            del data['customer_id']

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
        first_name = data.get('first_name')
        last_name = data.get('last_name')

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
            user = (
                User.objects.get(pk=user_id)
                if user_id is not None
                else None
            )
        except User.DoesNotExist:
            user = None

        # If the customer were created by our employees, just set password, other information have been filled.
        if customer_id is not None:
            try:
                customer = Customer.objects.get(pk=customer_id)
                if user is not None:
                    user.set_password(password)
                    user.save()
                    return Response({"message": _("Verified")}, status=HTTP_200_OK)
            except Customer.DoesNotExist:
                raise ValidationError({"detail": "The customer does not exist."})

        else:
            with transaction.atomic():
                if not user:
                    user = User.objects.create(
                        email=email,
                        password=make_password(password),
                        first_name=first_name,
                        last_name=last_name,
                        is_active=True
                    )
                else:
                    if password:
                        user.set_password(password)
                        user.save()
                customer = Customer.objects.create(
                    user=user,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    status=AccountStatus.ACTIVE
                )
        return Response({"message": _("Verified")}, status=HTTP_200_OK)
    
    @action(detail=False, methods=[Http.HTTP_POST], url_path="login", permission_classes=[AllowAny], authentication_classes=[])
    def login(self, request, pk=None):
        # Get data from JSON or POST
        username = request.data.get("username") or request.POST.get("username")
        password = request.data.get("password") or request.POST.get("password")
        
        if not username or not password:
            return Response({"error": _("Username and password are required.")}, status=HTTP_400_BAD_REQUEST)
        
        print(f"Login attempt - username: {username}, password: {password}")
        
        # Check if user exists and password is correct
        try:
            user = User.objects.prefetch_related("customers").get(email=username)
            print(f"Found user: {user.email}, id: {user.id}")
        except User.DoesNotExist:
            print(f"User not found: {username}")
            return Response(
                {"error": _("Invalid email or password.")},
                status=HTTP_400_BAD_REQUEST,
            )
        
        # Verify password
        password_check = user.check_password(password)
        print(f"Password check result: {password_check}")
        print(f"User password hash: {user.password}")
        
        if not password_check:
            print(f"Password verification failed for user: {username}")
            return Response(
                {"error": _("Invalid email or password.")},
                status=HTTP_400_BAD_REQUEST,
            )
        
        # Check if user has customer account
        customer = user.customers.first()
        if not customer:
            return Response(
                {"error": _("Customer account not found.")},
                status=HTTP_404_NOT_FOUND,
            )
        
        if customer.status != AccountStatus.ACTIVE:
            return Response(
                {"error": _("Customer account is not active.")},
                status=HTTP_400_BAD_REQUEST,
            )
        
        # For development, return simple token (you can replace with JWT or session)
        import secrets
        simple_token = secrets.token_urlsafe(32)
        
        # Store token in session or cache if needed
        request.session['customer_id'] = str(customer.id)
        request.session['user_id'] = str(user.id)
        request.session.save()  # Force save session
        
        # Store token mapping in Django cache for cross-origin requests
        from django.core.cache import cache
        cache.set(f'customer_token_{simple_token}', str(customer.id), timeout=3600)  # 1 hour
        print(f"Stored token mapping in cache: customer_token_{simple_token} -> {customer.id}")
        
        print(f"Login successful - stored session data:")
        print(f"  customer_id: {request.session.get('customer_id')}")
        print(f"  user_id: {request.session.get('user_id')}")
        print(f"  session_key: {request.session.session_key}")
        print(f"  session dict: {dict(request.session)}")
        
        customer_serializer = CustomerSerializer(customer)
        
        return Response({
            "message": _("Login successful!"),
            "customer": customer_serializer.data,
            "access_token": simple_token,
            "token_type": "Bearer",
            "expires_in": 3600
        }, status=HTTP_200_OK)

    @action(detail=False, methods=[Http.HTTP_POST], url_path="refresh-token", permission_classes=[AllowAny], authentication_classes=[])
    def refreshToken(self, request):
        refresh_token = request.data.get("refresh_token") or request.POST.get("refresh_token")
        if not refresh_token or refresh_token == 'null':
            return Response(
                {"error": _("Invalid token")},
                status=HTTP_406_NOT_ACCEPTABLE,
            )
        
        from django.http import QueryDict
        post_data = QueryDict('', mutable=True)
        post_data.update({
            "grant_type": "refresh_token",
            "client_id": BUSINESS_CLIENT_ID,
            "client_secret": BUSINESS_CLIENT_SECRET,
            "refresh_token": refresh_token,
        })
        request._request.POST = post_data
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
            CustomerService.send_forgot_password_email(email=email)
            return Response({"message": _("The link has been sent.")}, status=HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({"message": _("An error occurred.")}, status=HTTP_500_INTERNAL_SERVER_ERROR)
        
    
    
    
    @action(detail=False, methods=[Http.HTTP_POST], url_path="reset_password", permission_classes=[AllowAny], authentication_classes=[])
    def reset_password(self, request, *args, **kwargs):
        token = request.data.get("token")
        new_password = request.data.get("password")
        
        try:
            CustomerService.set_password(token=token, new_password=new_password)
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
            CustomerService.change_password(email=email, current_password=current_password, new_password=new_password)
            return Response({"message": _("Password has been changed.")}, status=HTTP_200_OK)

        except ValueError as ve:
            return Response({"message": str(ve)}, status=HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(e)
            return Response({"message": _("An error occurred.")}, status=HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=[Http.HTTP_GET], url_path="userinfo", permission_classes=[AllowAny], authentication_classes=[])
    def userinfo(self, request, *args, **kwargs):
        try:
            print(f"Userinfo request session: {dict(request.session)}")
            print(f"Userinfo request cookies: {request.COOKIES}")
            
            # Get customer ID from session (simplified for testing)
            customer_id = request.session.get('customer_id')
            
            # If no session, try to get from bearer token
            if not customer_id:
                auth_header = request.META.get('HTTP_AUTHORIZATION')
                if auth_header and auth_header.startswith('Bearer '):
                    token = auth_header.split(' ')[1]
                    print(f"Userinfo: Trying to find customer by token: {token}")
                    
                    # Look for customer ID by token in cache
                    from django.core.cache import cache
                    cache_key = f'customer_token_{token}'
                    customer_id = cache.get(cache_key)
                    print(f"Userinfo: Found customer_id from cache: {customer_id}")
            
            if not customer_id:
                print("No customer_id in session or cache")
                return Response({"error": _("Not authenticated"), "session": dict(request.session)}, status=HTTP_401_UNAUTHORIZED)
            
            print(f"Found customer_id in session: {customer_id}")
            customer = Customer.objects.get(id=customer_id)
            serializer = CustomerSerializer(customer)
            return Response({"customer": serializer.data}, status=HTTP_200_OK)
        except Customer.DoesNotExist:
            print(f"Customer with id {customer_id} not found")
            return Response({"error": _("Customer not found")}, status=HTTP_404_NOT_FOUND)
        except Exception as e:
            print(f"Userinfo error: {e}")
            return Response({"message": _("Customer not found.")}, status=HTTP_404_NOT_FOUND)

    @action(detail=False, methods=[Http.HTTP_PUT], url_path="profile", permission_classes=[AllowAny], authentication_classes=[])
    def update_profile(self, request, *args, **kwargs):
        try:
            print(f"Profile update request data: {request.data}")
            print(f"Profile update session: {request.session.get('customer_id')}")
            print(f"Authorization header: {request.META.get('HTTP_AUTHORIZATION')}")
            
            # Try to get customer ID from session first (for session-based auth)
            customer_id = request.session.get('customer_id')
            
            # If no session, try to get from bearer token
            if not customer_id:
                auth_header = request.META.get('HTTP_AUTHORIZATION')
                if auth_header and auth_header.startswith('Bearer '):
                    token = auth_header.split(' ')[1]
                    print(f"Trying to find customer by token: {token}")
                    
                    # Look for customer ID by token in cache
                    # This is a simple token mapping - in production use proper JWT validation
                    from django.core.cache import cache
                    cache_key = f'customer_token_{token}'
                    customer_id = cache.get(cache_key)
                    print(f"Found customer_id from cache: {customer_id}")
                    
                    if customer_id:
                        print(f"Successfully authenticated with token: {token}")
                    else:
                        print(f"Token {token} not found in cache")
            
            if not customer_id:
                return Response({"error": _("Not authenticated")}, status=HTTP_401_UNAUTHORIZED)
            
            customer = Customer.objects.get(id=customer_id)
            
            # Update customer fields
            customer.first_name = request.data.get("first_name", customer.first_name)
            customer.last_name = request.data.get("last_name", customer.last_name)
            customer.phone = request.data.get("phone", customer.phone)
            customer.address = request.data.get("address", customer.address)
            customer.province_id = request.data.get("province_id", customer.province_id)
            customer.district_id = request.data.get("district_id", customer.district_id)
            customer.ward_id = request.data.get("ward_id", customer.ward_id)
            customer.date_of_birth = request.data.get("date_of_birth", customer.date_of_birth)
            customer.gender = request.data.get("gender", customer.gender)
            
            # Update email if provided
            if request.data.get("email"):
                customer.email = request.data.get("email")
            
            customer.save()
            
            # Update user fields if user exists
            if customer.user:
                user = customer.user
                user.first_name = request.data.get("first_name", user.first_name)
                user.last_name = request.data.get("last_name", user.last_name)
                # Update email if provided
                if request.data.get("email"):
                    user.email = request.data.get("email")
                user.save()
            
            serializer = CustomerSerializer(customer)
            return Response({
                "message": _("Profile updated successfully!"),
                "customer": serializer.data
            }, status=HTTP_200_OK)
            
        except Customer.DoesNotExist:
            return Response({"error": _("Customer not found")}, status=HTTP_404_NOT_FOUND)
        except Exception as e:
            print(f"Profile update error: {e}")
            return Response({"message": _("Failed to update profile.")}, status=HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=[Http.HTTP_POST], url_path="change-password", permission_classes=[AllowAny], authentication_classes=[])
    def change_password(self, request, *args, **kwargs):
        try:
            print(f"Change password request data: {request.data}")
            
            # Get customer ID from session
            customer_id = request.session.get('customer_id')
            if not customer_id:
                return Response({"error": _("Not authenticated")}, status=HTTP_401_UNAUTHORIZED)
            
            customer = Customer.objects.get(id=customer_id)
            user = customer.user
            
            # Get passwords from request
            current_password = request.data.get("current_password")
            new_password = request.data.get("new_password")
            
            # Validation
            if not current_password or not new_password:
                return Response({"error": _("Current password and new password are required")}, status=HTTP_400_BAD_REQUEST)
            
            # Verify current password
            if not user.check_password(current_password):
                return Response({"error": _("Current password is incorrect")}, status=HTTP_400_BAD_REQUEST)
            
            # Validate new password length
            if len(new_password) < 6:
                return Response({"error": _("New password must be at least 6 characters")}, status=HTTP_400_BAD_REQUEST)
            
            # Update password
            user.set_password(new_password)
            user.save()
            
            print(f"Password changed successfully for customer: {customer_id}")
            
            return Response({
                "message": _("Password changed successfully!")
            }, status=HTTP_200_OK)
            
        except Customer.DoesNotExist:
            return Response({"error": _("Customer not found")}, status=HTTP_404_NOT_FOUND)
        except Exception as e:
            print(f"Change password error: {e}")
            return Response({"message": _("Failed to change password.")}, status=HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=[Http.HTTP_GET], url_path="scopes", permission_classes=[IsAuthenticated])
    def scopes(self, request, pk=None):
        try:
            user = request.user
            customer = user.customers.first()
            if not customer:
                return Response({"error": _("Customer not found")}, status=HTTP_404_NOT_FOUND)
            
            # Customer scopes
            scopes = ['ecommerce:orders:view-mine', 'ecommerce:orders:edit-mine', 'ecommerce:products:view']
            return Response({"scopes": scopes}, status=HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"message": _("An error occurred.")}, status=HTTP_500_INTERNAL_SERVER_ERROR)