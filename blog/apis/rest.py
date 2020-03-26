from typing import Dict, Tuple

from loguru import logger

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import exceptions, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.request import Request
from rest_framework.response import Response

from .. import interfaces
from .. import permissions as custom_permissions
from .. import serializers, services
from ..filter import PostFilter


class PostViewSet(viewsets.ModelViewSet):

    queryset = services.PostService().get_all_published_posts()

    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)

    filterset_class = PostFilter

    search_fields = ("title", "description")

    ordering = ("-published_at",)

    ordering_fields = ("tags__name", "published_at", "read_time")

    lookup_field = "slug"

    def get_serializer_class(self, *args: Tuple, **kwargs: Dict):

        if self.action == "create":
            return serializers.PostCreateUpdateSerializer

        if self.action == "retrieve":
            return serializers.PostSerializer

        if self.action == "update" or self.action == "partial_update":
            return serializers.PostCreateUpdateSerializer

        return serializers.PostListSerializer

    def get_permissions(self):

        if self.action == "create":

            permission_classes = (permissions.IsAuthenticated,)

        elif self.action == "update" or self.action == "partial_update":

            permission_classes = (
                permissions.IsAuthenticatedOrReadOnly,
                custom_permissions.IsOwnerOrReadOnly,
            )

        elif self.action == "destroy":

            permission_classes = (
                permissions.IsAuthenticatedOrReadOnly,
                custom_permissions.IsOwnerOrReadOnly,
            )

        else:

            permission_classes = [permissions.IsAuthenticatedOrReadOnly]

        return [permission() for permission in permission_classes]

    @action(detail=False, methods=["GET"], name="My Drafted Post")
    def draft(self, request: Request) -> Response:

        posts = services.PostService().get_all_draft_posts_by_author(
            author_id=request.user.user_uuid
        )

        serializer = self.get_serializer(posts, many=True)

        logger.info(f"Getting all {request.user} Draft Post")

        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request: Request, *args, **kwargs):
        if request.user.is_authenticated:

            try:

                post = services.PostService().get_post(
                    author_id=request.user.user_uuid, slug=kwargs.get("slug")
                )

                serializer = self.get_serializer(post)

                interfaces.AnalyticInterface().create_analytic(
                    model=post.__class__, instance=post, request=request
                )

                return Response(serializer.data, status=status.HTTP_200_OK)

            except Exception as error:
                logger.error(error)
                raise exceptions.ValidationError(
                    detail={"detail": "Not Found"}, code="not found"
                )

        else:

            try:

                post = services.PostService().get_post(slug=kwargs.get("slug"))

                serializer = serializers.PostSerializer(post)

                return Response(serializer.data, status=status.HTTP_200_OK)

            except Exception as error:
                logger.error(error)

                raise exceptions.ValidationError(
                    detail={"detail": "Not Found"}, code="not found"
                )

    def perform_create(self, serializer):

        serializer.save(author=self.request.user.user_uuid)


class TagViewSet(viewsets.ModelViewSet):

    queryset = services.TagService().get_all_tags()

    serializer_class = serializers.TagSerializer
