from django_filters import rest_framework as filters

from .models import Post


class PostFilter(filters.FilterSet):

    tags_name = filters.CharFilter("tags__name")

    published_at = filters.DateFromToRangeFilter("published_at")

    class Meta:
        model = Post
        fields = (
            "tags_name",
            "read_time",
            "published_at",
        )
