"""users REST API URL Configuration"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .apis import rest

router = DefaultRouter()
router.register("", rest.UserViewSet)

app_name = "users"

urlpatterns = [
    path("", include(router.urls)),
]
