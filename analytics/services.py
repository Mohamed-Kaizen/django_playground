from django.contrib.contenttypes.models import ContentType

from .models import Analytic


class AnalyticService:

    @staticmethod
    def get_all_users() -> Analytic:
        return Analytic.objects.all()

    @staticmethod
    def filter_by_content_type(*, content_type: ContentType) -> Analytic:
        return Analytic.objects.filter(content_type=content_type)

