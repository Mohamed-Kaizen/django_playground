from django.utils.translation import gettext_lazy as _
from graphene_django import DjangoObjectType

from .models import CustomUser


class UserType(DjangoObjectType):
    class Meta:
        description = _("Type definition for user model")
        model = CustomUser
        exclude = ("password", "is_superuser", "last_name", "first_name", "id")
