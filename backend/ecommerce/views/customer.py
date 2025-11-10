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
    ECOMMERCE_CLIENT_ID,
    ECOMMERCE_CLIENT_SECRET,
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
        
        try:
            customer = Customer.objects.get(email=email)
            return Response({"detail": "A customer account with that email already exists."}, status=HTTP_400_BAD_REQUEST)
        except Customer.DoesNotExist:
            pass  
        
        try:
            with transaction.atomic():
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
                
                customer = Customer.objects.create(
                    user=user,
                    email=email,
                    first_name=first_name or "",
                    last_name=last_name or "",
                    status=AccountStatus.ACTIVE
                )
                
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
        # Log raw request data for debugging
        print(f"[LOGIN] Raw request.data: {request.data}")
        print(f"[LOGIN] Raw request.POST: {request.POST}")
        
        username = request.data.get("username") or request.POST.get("username")
        password = request.data.get("password") or request.POST.get("password")
        
        print(f"[LOGIN] Received username: '{username}', password: '{password}'")
        print(f"[LOGIN] Username length: {len(username) if username else 0}, Password length: {len(password) if password else 0}")
        
        if not username or not password or username.strip() == "" or password.strip() == "":
            print("[LOGIN] Username or password missing or empty")
            # Clear session and revoke old token to prevent confusion
            try:
                old_access_token = request.session.get('access_token')
                if old_access_token:
                    from django.http import QueryDict
                    post_data = QueryDict('', mutable=True)
                    post_data.update({
                        "client_id": ECOMMERCE_CLIENT_ID,
                        "client_secret": ECOMMERCE_CLIENT_SECRET,
                        "token_type_hint": "access_token",
                        "token": old_access_token,
                    })
                    request._request.POST = post_data
                    self.create_revocation_response(request._request)  # Revoke old token
                    print(f"[LOGIN] Revoked old access token on validation fail")
                    
                    # Also clear the cache for the old token
                    try:
                        from django.core.cache import cache
                        import hashlib
                        old_token_hash = hashlib.sha256(old_access_token.encode()).hexdigest()
                        old_cache_key = f'customer_token_{old_token_hash}'
                        cache.delete(old_cache_key)
                        print(f"[LOGIN] Cleared cache for old token on validation fail")
                    except Exception as e:
                        print(f"[LOGIN] Failed to clear cache for old token: {e}")
                
                request.session.flush()
            except Exception:
                pass
            return Response({"error": _("Username and password are required.")}, status=HTTP_400_BAD_REQUEST)
        
        # Clear any existing session data to prevent cross-contamination
        try:
            # Revoke old access token if exists
            old_access_token = request.session.get('access_token')
            if old_access_token:
                from django.http import QueryDict
                post_data = QueryDict('', mutable=True)
                post_data.update({
                    "client_id": ECOMMERCE_CLIENT_ID,
                    "client_secret": ECOMMERCE_CLIENT_SECRET,
                    "token_type_hint": "access_token",
                    "token": old_access_token,
                })
                request._request.POST = post_data
                self.create_revocation_response(request._request)  # Revoke old token
                print(f"[LOGIN] Revoked old access token")
                
                # Also clear the cache for the old token
                try:
                    from django.core.cache import cache
                    import hashlib
                    old_token_hash = hashlib.sha256(old_access_token.encode()).hexdigest()
                    old_cache_key = f'customer_token_{old_token_hash}'
                    cache.delete(old_cache_key)
                    print(f"[LOGIN] Cleared cache for old token")
                except Exception as e:
                    print(f"[LOGIN] Failed to clear cache for old token: {e}")
            
            request.session.flush()
        except Exception as e:
            print(f"[LOGIN] Warning: Could not flush session: {e}")
        
        try:
            user = User.objects.prefetch_related("customers").get(email=username)
        except User.DoesNotExist:
            return Response({"error": _("Invalid email or password.")}, status=HTTP_400_BAD_REQUEST)
        
        if not user.check_password(password):
            return Response({"error": _("Invalid email or password.")}, status=HTTP_400_BAD_REQUEST)
        
        customer = user.customers.first()
        if not customer:
            return Response({"error": _("Customer account not found.")}, status=HTTP_404_NOT_FOUND)
        if customer.status != AccountStatus.ACTIVE:
            return Response({"error": _("Customer account is not active.")}, status=HTTP_400_BAD_REQUEST)
        
        print(f"[LOGIN] Authenticating customer: {customer.id} ({customer.email})")

        # Exchange credentials for OAuth2 access/refresh tokens
        # Ensure requested scope is within the application's allowed scopes to avoid invalid_scope
        try:
            from oauth.models import Application
            app = Application.objects.filter(client_id=ECOMMERCE_CLIENT_ID).first()
            app_scope = app.scope if app else ''
        except Exception:
            app_scope = ''
        
        # Update request._request.POST (the underlying Django request, not DRF's request.POST)
        request._request.POST._mutable = True
        request._request.POST.update({
            "grant_type": "password",
            "client_type": "confidential",
            "client_id": ECOMMERCE_CLIENT_ID,
            "client_secret": ECOMMERCE_CLIENT_SECRET,
            "username": username,
            "password": password,
        })
        if app_scope:
            request._request.POST.update({"scope": app_scope})
        
        url, headers, body, status = self.create_token_response(request._request)
        try:
            token_payload = json.loads(body)
        except Exception:
            token_payload = {}
        if status != 200:
            return Response(token_payload or {"error": _("Login failed")}, status=status)

        # Cache the access token to customer_id mapping
        access_token = token_payload.get('access_token')
        if access_token:
            try:
                from django.core.cache import cache
                import hashlib
                # Hash the token to avoid cache key length issues
                token_hash = hashlib.sha256(access_token.encode()).hexdigest()
                cache_key = f'customer_token_{token_hash}'
                # Cache for the same duration as the access token (default 1 hour = 3600 seconds)
                expires_in = token_payload.get('expires_in', 3600)
                cache.set(cache_key, str(customer.id), timeout=expires_in)
                print(f"[LOGIN] Cached customer_id {customer.id} for token hash (expires in {expires_in}s)")
            except Exception as e:
                print(f"[LOGIN] Failed to cache token: {e}")

        # Optionally set session for convenience
        try:
            request.session['customer_id'] = str(customer.id)
            request.session['user_id'] = str(user.id)
            if access_token:
                request.session['access_token'] = access_token
            request.session.save()
        except Exception:
            pass

        customer_serializer = CustomerSerializer(customer)
        customer_data = customer_serializer.data
        
        print(f"[LOGIN] Returning customer data: ID={customer_data.get('id')}, Email={customer_data.get('email')}")
        
        token_payload.update({
            "message": _("Login successful!"),
            "customer": customer_data,
        })
        return Response(token_payload, status=HTTP_200_OK)

    @action(detail=False, methods=[Http.HTTP_POST], url_path="refresh", permission_classes=[AllowAny], authentication_classes=[])
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
            "client_id": ECOMMERCE_CLIENT_ID,
            "client_secret": ECOMMERCE_CLIENT_SECRET,
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
        # Use request.data for POST body (works with DRF), not request.POST
        refresh_token = request.data.get("refresh_token") or request.POST.get("refresh_token")
        access_token = request.data.get("access_token") or request.POST.get("access_token")
        
        # Clear cache for access token FIRST before revoking
        if access_token:
            try:
                from django.core.cache import cache
                import hashlib
                token_hash = hashlib.sha256(access_token.encode()).hexdigest()
                cache_key = f'customer_token_{token_hash}'
                cache.delete(cache_key)
                print(f"[LOGOUT] Cleared cache for access token")
            except Exception as e:
                print(f"[LOGOUT] Failed to clear cache: {e}")
        
        # Create a mutable copy for OAuth revocation
        from django.http import QueryDict
        post_data = QueryDict('', mutable=True)
        post_data.update({
            "client_id": ECOMMERCE_CLIENT_ID,
            "client_secret": ECOMMERCE_CLIENT_SECRET,
            "token_type_hint": "refresh_token",
            "token": refresh_token,
        })
        request._request.POST = post_data
        url, headers, body, status = self.create_revocation_response(request._request)
        if status != HTTP_200_OK:
            print(f"[LOGOUT] Failed to revoke refresh token, status: {status}")
            # Don't return error, continue to revoke access token

        post_data = QueryDict('', mutable=True)
        post_data.update({
            "client_id": ECOMMERCE_CLIENT_ID,
            "client_secret": ECOMMERCE_CLIENT_SECRET,
            "token_type_hint": "access_token",
            "token": access_token,
        })
        request._request.POST = post_data
        url, headers, body, status = self.create_revocation_response(request._request)
        if status != HTTP_200_OK:
            print(f"[LOGOUT] Failed to revoke access token, status: {status}")
            # Don't return error, continue to clear session

        try:
            request.session.flush()
            print(f"[LOGOUT] Session flushed successfully")
        except Exception as e:
            print(f"[LOGOUT] Error flushing session: {e}")
        
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
            
            customer_id = None
            auth_header = request.META.get('HTTP_AUTHORIZATION')
            if auth_header and auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
                print(f"Userinfo: Trying to find customer by token")
                from django.core.cache import cache
                import hashlib
                token_hash = hashlib.sha256(token.encode()).hexdigest()
                cache_key = f'customer_token_{token_hash}'
                customer_id = cache.get(cache_key)
                print(f"Userinfo: Found customer_id from cache: {customer_id}")

            if not customer_id:
                customer_id = request.session.get('customer_id')
            
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
            
            customer_id = None
            auth_header = request.META.get('HTTP_AUTHORIZATION')
            if auth_header and auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
                print(f"Trying to find customer by token")
                from django.core.cache import cache
                import hashlib
                token_hash = hashlib.sha256(token.encode()).hexdigest()
                cache_key = f'customer_token_{token_hash}'
                customer_id = cache.get(cache_key)
                print(f"Found customer_id from cache: {customer_id}")
                if customer_id:
                    print(f"Successfully authenticated with token")
                else:
                    print(f"Token not found in cache")
            
            if not customer_id:
                customer_id = request.session.get('customer_id')
            
            if not customer_id:
                return Response({"error": _("Not authenticated")}, status=HTTP_401_UNAUTHORIZED)
            
            customer = Customer.objects.get(id=customer_id)
            
            customer.first_name = request.data.get("first_name", customer.first_name)
            customer.last_name = request.data.get("last_name", customer.last_name)
            customer.phone = request.data.get("phone", customer.phone)
            customer.address = request.data.get("address", customer.address)
            customer.avatar = request.data.get("avatar", customer.avatar)
            customer.province_id = request.data.get("province_id", customer.province_id)
            customer.district_id = request.data.get("district_id", customer.district_id)
            customer.ward_id = request.data.get("ward_id", customer.ward_id)
            customer.date_of_birth = request.data.get("date_of_birth", customer.date_of_birth)
            customer.gender = request.data.get("gender", customer.gender)
            
            if request.data.get("email"):
                customer.email = request.data.get("email")
            
            customer.save()
            
            if customer.user:
                user = customer.user
                user.first_name = request.data.get("first_name", user.first_name)
                user.last_name = request.data.get("last_name", user.last_name)
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
            
            customer_id = None
            auth_header = request.META.get('HTTP_AUTHORIZATION')
            if auth_header and auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
                from django.core.cache import cache
                import hashlib
                token_hash = hashlib.sha256(token.encode()).hexdigest()
                cache_key = f'customer_token_{token_hash}'
                customer_id = cache.get(cache_key)
            if not customer_id:
                customer_id = request.session.get('customer_id')
            if not customer_id:
                return Response({"error": _("Not authenticated")}, status=HTTP_401_UNAUTHORIZED)

            customer = Customer.objects.get(id=customer_id)
            user = customer.user
            
            current_password = request.data.get("current_password")
            new_password = request.data.get("new_password")
            
            if not current_password or not new_password:
                return Response({"error": _("Current password and new password are required")}, status=HTTP_400_BAD_REQUEST)
            
            if not user.check_password(current_password):
                return Response({"error": _("Current password is incorrect")}, status=HTTP_400_BAD_REQUEST)
            
            if len(new_password) < 6:
                return Response({"error": _("New password must be at least 6 characters")}, status=HTTP_400_BAD_REQUEST)
            
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
            
            scopes = ['ecommerce:orders:view-mine', 'ecommerce:orders:edit-mine', 'ecommerce:products:view']
            return Response({"scopes": scopes}, status=HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"message": _("An error occurred.")}, status=HTTP_500_INTERNAL_SERVER_ERROR)