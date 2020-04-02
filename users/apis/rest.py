# from typing import Dict, Tuple, List
#
# from django.db.utils import IntegrityError
# from django.utils.translation import gettext_lazy as _
# from rest_framework import exceptions, permissions, status, viewsets
# from rest_framework.decorators import action
# from rest_framework.request import Request
# from rest_framework.response import Response
#
# from .. import permissions as custom_permissions
# from .. import serializers, services
#
#
# class UserViewSet(viewsets.ModelViewSet):
#     queryset = services.UserService().get_all_users()
#
#     lookup_field = "username"
#
#     def get_serializer_class(self, *args: Tuple, **kwargs: Dict):
#
#         if self.action == "create":
#             return serializers.UserCreateSerializer
#
#         if self.action == "retrieve":
#             return serializers.UserRetrieveSerializer
#
#         if self.action == "password":
#             return serializers.UserChangePasswordSerializer
#
#         if self.action == "update" or self.action == "partial_update":
#             return serializers.UserUpdateSerializer
#
#         return serializers.UserListSerializer
#
#     def get_permissions(self):
#
#         if self.action == "create":
#
#             permission_classes = (custom_permissions.IsNotAuthenticated,)
#
#         elif (
#             self.action == "update"
#             or self.action == "partial_update"
#             or self.action == "password"
#         ):
#
#             permission_classes = (
#                 permissions.IsAuthenticatedOrReadOnly,
#                 custom_permissions.IsOwnerOrReadOnly,
#             )
#
#         elif self.action == "destroy":
#
#             permission_classes = (permissions.IsAdminUser,)
#
#         else:
#
#             permission_classes = [permissions.IsAuthenticatedOrReadOnly]
#
#         return [permission() for permission in permission_classes]
#
#     @action(detail=True, methods=["PUT", "PATCH"], name="Change User Password")
#     def password(self, request: Request, username: str) -> Response:
#
#         serializer = self.get_serializer(data=request.data)
#
#         if serializer.is_valid(raise_exception=True):
#
#             old_password = serializer.data.get("old_password")
#
#             new_password = serializer.data.get("new_password")
#
#             retype_new_password = serializer.data.get("retype_new_password")
#
#             success = request.user.check_password(old_password)
#
#             if success and new_password == retype_new_password:
#                 request.user.set_password(new_password)
#
#                 request.user.save()
#
#                 return Response(
#                     {"detail": "Your password has been changed"},
#                     status=status.HTTP_201_CREATED,
#                 )
#         else:
#             return Response(
#                 {"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
#             )
#
#     def create(self, request: Request, *args: Tuple, **kwargs: Dict) -> Response:
#
#         serializer = self.get_serializer(data=request.data)
#
#         if serializer.is_valid(raise_exception=True):
#
#             try:
#
#                 services.UserService().create_user(data=serializer.data)
#
#                 return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#             except IntegrityError as error:
#
#                 if ".email" in f"{error}":
#                     raise exceptions.ValidationError(
#                         {"email": _("Email Already Exists")}, code=_("invalid")
#                     )
#
#                 if ".username" in f"{error}":
#                     raise exceptions.ValidationError(
#                         {"username": _("UserName Already Exists")}, code=_("invalid")
#                     )
#
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
