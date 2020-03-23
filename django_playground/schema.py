import graphene
from graphene_django.debug import DjangoDebug
from users.schema import UserQuery


class Query(UserQuery, graphene.ObjectType):
    debug = graphene.Field(DjangoDebug, name="_debug")


schema = graphene.Schema(query=Query)
