from django.urls import path, include
from rest_framework_nested import routers
from base.routers import MutipleUpdateRouter
from .views import (
    EmployeeCustomFieldViewSet,
    EmployeeViewSet,
    EmployeeAdditionalInformationViewSet
)

router = MutipleUpdateRouter(trailing_slash=False)
router.register(r'employee-custom-fields', EmployeeCustomFieldViewSet, basename="employee-custom-fields")
router.register(r'employees', EmployeeViewSet, basename="employees")
employee_router = routers.NestedSimpleRouter(router, r'employees', lookup='employees')
employee_router.register(r'additional-information', EmployeeAdditionalInformationViewSet, basename="additional-information")

urlpatterns = [
    path(r'api/v1/', include(router.urls)),
    path(r'api/v1/', include(employee_router.urls))
]
