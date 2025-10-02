from django.urls import re_path, include, path
from rest_framework_nested import routers
from base import routers

from .views import (
    GroupViewSet,
    OfficeViewSet,
    HolidayViewSet,
    WorkSessionViewSet,
    UnitViewSet,
    UnitTypeViewSet
)

app_name = "hr"
router = routers.MutipleUpdateRouter(trailing_slash=False)

router.register(r'groups', GroupViewSet, basename="groups")
router.register(r'offices', OfficeViewSet, basename="offices")
router.register(r'units', UnitViewSet, basename="units")
router.register(r'unit-types', UnitTypeViewSet, basename="unit-types")

group_router = routers.NestedMutipleUpdateRouter(router, r'groups', lookup='group')
group_router.register(r'offices', OfficeViewSet, basename="offices")

office_router = routers.NestedMutipleUpdateRouter(group_router, r'offices', lookup='office')
office_router.register(r'holidays', HolidayViewSet, basename="holidays")
office_router.register(r'work-sessions', WorkSessionViewSet, basename="work-sessions")

office_router_non_group = routers.NestedMutipleUpdateRouter(router, r'offices', lookup='office')
office_router_non_group.register(r'holidays', HolidayViewSet, basename="holidays")
office_router_non_group.register(r'work-sessions', WorkSessionViewSet, basename="work-sessions")

urlpatterns = [
    re_path(r'^api/v1/', include(router.urls)),
    re_path(r'^api/v1/', include(group_router.urls)),
    re_path(r'^api/v1/', include(office_router.urls)),
    re_path(r'^api/v1/', include(office_router_non_group.urls)),

]
