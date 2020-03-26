"""blog URL Configuration"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .apis import rest

router = DefaultRouter()

router.register("posts", rest.PostViewSet)
router.register("tags", rest.TagViewSet)

app_name = "blog"

urlpatterns = [
    path("", include(router.urls)),
]
