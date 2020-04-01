"""blog URL Configuration"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .apis import rest

# router = DefaultRouter()
#
# router.register("assignment", rest.AssignmentViewSet)


app_name = "e_learning"

urlpatterns = [
    # path("", include(router.urls)),
    # path("grade/", rest.grade),
]
