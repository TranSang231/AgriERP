"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from os.path import dirname, join
from django.urls import include, re_path, path
from .static import static
from .settings.base import (
    STATIC_URL,
    STATIC_ROOT,
    MEDIA_URL,
    MEDIA_ROOT,
    LOCAL_BUILD,
    DEBUG,
    BUSINESS_FRONTEND_DEV_MODE,
    DOCS_FRONTEND_DEV_MODE,
    BUSINESS_STATIC,
    DOCS_STATIC,
    DEFAULT_FILE_STORAGE
)

from .views import single_page_view
from health_check.urls import urlpatterns as health_check_urls
from .constants_urls import urlpatterns as constants_urls

urlpatterns = [
    # path('admin/', admin.site.urls),
    path(r'', include(constants_urls)),
    path(r'', include('oauth.urls')),
    path(r'', include('otp.urls')),
    path(r'', include('businesses.urls')),
    path(r'', include('hr.urls')),
	path(r'', include('knowledge.urls')),
    path(r'', include('websites.urls')),
    path(r'', include('va.urls')),
    path(r'', include('ecommerce.urls')),
    path(r'', include('contents.urls')),
    path(r'', include('supplier_management.urls'))
    # path(r'', include('firebase.urls'))
]
# Static route
urlpatterns += static(STATIC_URL, document_root=STATIC_ROOT)
if LOCAL_BUILD and not BUSINESS_FRONTEND_DEV_MODE:
    urlpatterns += static("/static/business/", document_root=BUSINESS_STATIC)
if LOCAL_BUILD and not DOCS_FRONTEND_DEV_MODE:
    urlpatterns += static("/static/admin/", document_root=DOCS_STATIC)

if DEFAULT_FILE_STORAGE == "binary_database_files.storage.DatabaseStorage":
    urlpatterns += [
        re_path(r'^api/v1/', include('binary_database_files.urls')),
    ]
if LOCAL_BUILD and not DEBUG:
    urlpatterns += static(STATIC_URL, documents_root=STATIC_ROOT)
    urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
urlpatterns += [
    re_path(r"^healthcheck/", include(health_check_urls)),
    re_path(r"^.*$", single_page_view),
]
