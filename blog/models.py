import datetime
from typing import Dict

from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .interfaces import AuthorInterface
from .utils import get_read_time, unique_slug


class Status(models.TextChoices):

    Draft = ("Draft", _("Draft"))

    Published = ("Published", _("Published"))


class Tag(models.Model):

    name = models.CharField(verbose_name=_("name"), max_length=200, unique=True)

    class Meta:
        verbose_name = _("tag")
        verbose_name_plural = _("tags")

    def __str__(self):
        return f"{self.name}"

    def total_posts(self):
        return self.posts.count()

    total_posts.short_description = _("Posts")
    total_posts.int = 0


class Post(models.Model):

    title = models.CharField(verbose_name=_("title"), max_length=400)

    description = models.TextField(verbose_name=_("description"))

    author = models.UUIDField(verbose_name=_("author"))

    tags = models.ManyToManyField(Tag, related_name="posts", verbose_name=_("tags"))

    status = models.CharField(
        verbose_name=_("status"),
        max_length=15,
        choices=Status.choices,
        default=Status.Draft,
    )

    read_time = models.IntegerField(default=0, verbose_name=_("read time"))

    slug = models.SlugField(verbose_name=_("slug"), unique=True, blank=True)

    published_at = models.DateTimeField(verbose_name=_("published at"))

    created_at = models.DateTimeField(verbose_name=_("created at"), auto_now_add=True)

    class Meta:

        verbose_name = _("post")

        verbose_name_plural = _("posts")

    def __str__(self):
        return f"{self.title}"

    def was_published_recently(self):
        """
        display post within 24 hours
        """
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.published_at <= now

    def author_name(self):
        return AuthorInterface().get_author(author_id=self.author).get("author_name")

    was_published_recently.admin_order_field = "published_at"
    was_published_recently.boolean = True
    was_published_recently.short_description = "Published recently?"


@receiver(pre_save, sender=Post)
def post_slug_creator(sender: Post, instance: Post, **kwargs: Dict) -> None:

    if not instance.slug:
        instance.slug = unique_slug(title=instance.title)

    if instance.description:
        instance.read_time = get_read_time(words=instance.description)
