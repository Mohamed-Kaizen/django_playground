from typing import Any

import graphene
from django.utils.translation import gettext_lazy as _
from graphene_django.views import GraphQLError

from .selectors import get_all_users, get_user_by_username
from .types import UserType


class UserQuery(graphene.ObjectType):

    current_user = graphene.Field(
        UserType, description=_("Current logged in User query")
    )

    users = graphene.List(UserType, description=_("All Users query"))

    user = graphene.Field(
        UserType, username=graphene.String(), description=_("Get Single User query")
    )

    @staticmethod
    def resolve_current_user(root: None, info: graphene.ResolveInfo) -> Any:
        """get current logged in user"""

        user = info.context.user

        if user.is_anonymous:
            raise GraphQLError(_("You Need To Be Authenticated"))

        return user

    @staticmethod
    def resolve_user(root: None, info: graphene.ResolveInfo, username: str) -> Any:
        """get user information"""

        return get_user_by_username(username=username)

    @staticmethod
    def resolve_users(root: None, info: graphene.ResolveInfo) -> Any:
        """get all user"""

        return get_all_users()
