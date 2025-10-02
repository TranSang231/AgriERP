from django.urls import include, re_path, path
from .views.constants import *

constants_routes = [
    path(r"", index, name="constants_list"),
    path(r"/<name>", retrieve, name="constant_detail")
]

urlpatterns = [
    re_path(r'^api/v1/constants', include(constants_routes)),
    re_path(r'^api/public/v1/constants', include(constants_routes)),
]



