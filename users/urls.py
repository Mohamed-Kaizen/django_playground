"""users REST API URL Configuration"""

from .apis import rest
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('', rest.UserViewSet)

app_name = "users"

urlpatterns = [
    path('', include(router.urls)),
]
