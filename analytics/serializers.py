from rest_framework import serializers

from .models import Analytic


class AnalyticSerializers(serializers.ModelSerializer):
    username = serializers.StringRelatedField(source="user")
    content_type = serializers.StringRelatedField()
    content_object = serializers.StringRelatedField()

    class Meta:
        model = Analytic
        fields = (
            "user",
            "username",
            "content_type",
            "object_id",
            "content_object",
            "action",
            "created_at",
            "device",
            "language",
        )
