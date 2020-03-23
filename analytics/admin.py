from django.contrib import admin
from import_export import resources
from import_export.admin import ExportActionModelAdmin

from .models import Analytic


class AnalyticResource(resources.ModelResource):
    class Meta:
        model = Analytic
        fields = (
            "user",
            "content_type__model",
            "object_id",
            "action",
            "language",
            "device",
            "created_at",
        )

        export_order = (
            "user",
            "content_type__model",
            "object_id",
            "action",
            "language",
            "device",
            "created_at",
        )


class AnalyticAdmin(ExportActionModelAdmin, admin.ModelAdmin):

    resource_class = AnalyticResource

    list_display = (
        "user",
        "content_type",
        "object_id",
        "content_object",
        "action",
        "language",
        "device",
        "created_at",
    )


admin.site.register(Analytic, AnalyticAdmin)
