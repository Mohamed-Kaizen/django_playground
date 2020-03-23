import json

from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed


@method_decorator(csrf_exempt, name="dispatch")
@method_decorator(staff_member_required, name="dispatch")
class StaffGraphQLView(GraphQLView):
    pass


class GraphQLTokenView(GraphQLView):
    # authentication_classes = [TokenAuthentication]

    def authenticate_request(self, request):
        for auth_class in self.authentication_classes:
            auth_tuple = auth_class().authenticate(request)

            if auth_tuple:
                request.user, request.token = auth_tuple
                break

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        try:
            self.authenticate_request(request)

        except AuthenticationFailed as auth_failed_error:
            return HttpResponse(
                json.dumps({"errors": [f"{auth_failed_error}"]}),
                status=status.HTTP_401_UNAUTHORIZED,
                content_type="application/json",
            )

        return super(GraphQLTokenView, self).dispatch(request, *args, **kwargs)
