from django.contrib.contenttypes.models import ContentType
from rest_framework import response, status
from rest_framework.decorators import api_view

from .. import serializers, services


@api_view(["GET"])
def analytics(request, model):

    try:

        ct = ContentType.objects.get(model=f"{model}")

        analytical = services.AnalyticService().filter_by_content_type(content_type=ct)

        serializer = serializers.AnalyticSerializers(analytical, many=True)

        return response.Response(serializer.data, status=status.HTTP_200_OK)

    except Exception:

        return response.Response(
            {"detail", "Not Found"}, status=status.HTTP_404_NOT_FOUND
        )
