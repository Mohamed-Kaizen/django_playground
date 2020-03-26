import uuid

from loguru import logger

from .models import Post, Status, Tag


class PostService:
    @staticmethod
    def get_all_published_posts() -> Post:
        return Post.objects.filter(status=Status.Published)

    @staticmethod
    def get_all_draft_posts_by_author(*, author_id: uuid.UUID) -> Post:
        return Post.objects.filter(status=Status.Draft, author=author_id)

    @staticmethod
    def get_post(*, author_id: uuid.UUID = None, slug: str) -> Post:
        post = Post.objects.get(slug=slug)

        if post.author == author_id:

            logger.success(f"Getting {post} for user {author_id}")

            return post

        else:
            return Post.objects.get(slug=slug, status=Status.Published)


class TagService:
    @staticmethod
    def get_all_tags() -> Tag:
        return Tag.objects.all()

    @staticmethod
    def get_or_create_tag(*, data: str) -> int:
        tag, created = Tag.objects.get_or_create(name=data.lower())

        if created:

            logger.success(f"{tag} was created")

        else:

            logger.success(f"getting {tag}")

        return tag.id
