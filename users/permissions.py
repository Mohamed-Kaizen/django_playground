from typing import Any

from django.utils.translation import gettext_lazy as _
from rest_framework import permissions
from rest_framework.request import Request


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: Any, obj: Any) -> bool:

        if request.method in permissions.SAFE_METHODS:
            return True

        return obj == request.user


class IsNotAuthenticated(permissions.BasePermission):
    """
    Allows access only to unauthenticated users.
    """

    message = _("You are authenticated.")

    def has_permission(self, request: Request, view: Any) -> bool:
        return not bool(request.user and request.user.is_authenticated)
