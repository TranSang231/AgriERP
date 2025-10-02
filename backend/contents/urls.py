from django.urls import include, re_path
from rest_framework.routers import SimpleRouter
from .views import LongContentViewSet, ShortContentViewSet, AttachmentViewSet

app_name = "contents"
router = SimpleRouter(trailing_slash=False) 

router.register("long-contents", LongContentViewSet, basename="long-contents")
router.register("short-contents", ShortContentViewSet, basename= "short-contents")
router.register("attachments", AttachmentViewSet, basename= "attachments")
urlpatterns = [
    re_path(r'^api/v1/', include(router.urls))
]
