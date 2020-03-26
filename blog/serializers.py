from rest_framework import serializers

from .models import Post
from .services import TagService


class TagStringSerializer(serializers.StringRelatedField):
    def to_internal_value(self, data: str) -> int:

        get_tag_id = TagService().get_or_create_tag(data=data)

        return get_tag_id


class PostListSerializer(serializers.Serializer):

    title = serializers.CharField(read_only=True)

    author = serializers.CharField(read_only=True, source="author_name")

    tags = serializers.StringRelatedField(read_only=True, many=True)

    read_time = serializers.IntegerField(read_only=True)

    slug = serializers.SlugField(read_only=True)

    status = serializers.CharField(read_only=True)

    published_at = serializers.DateTimeField(read_only=True)

    was_published_recently = serializers.BooleanField(read_only=True)


class PostSerializer(serializers.Serializer):

    title = serializers.CharField(read_only=True)

    description = serializers.CharField(read_only=True)

    author = serializers.CharField(read_only=True, source="author_name")

    tags = serializers.StringRelatedField(read_only=True, many=True)

    read_time = serializers.IntegerField(read_only=True)

    published_at = serializers.DateTimeField(read_only=True)


class PostCreateUpdateSerializer(serializers.ModelSerializer):

    tags = TagStringSerializer(many=True)

    class Meta:
        model = Post
        fields = ("title", "description", "tags", "status", "published_at")


class TagSerializer(serializers.Serializer):

    name = serializers.CharField(read_only=True)

    total_posts = serializers.IntegerField(read_only=True)
