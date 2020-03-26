from django.contrib import admin

from .models import Post, Tag


class PostAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "author_name",
        "status",
        "read_time",
        "published_at",
        "created_at",
    )

    ordering = (
        "title",
        "status",
        "read_time",
        "published_at",
        "created_at",
    )

    list_filter = ("status", "read_time", "published_at", "created_at")

    search_fields = ("title", "author_name", "description")


class TagAdmin(admin.ModelAdmin):

    list_display = ("name", "total_posts")

    ordering = ("name",)

    search_fields = ("name",)


admin.site.register(Post, PostAdmin)
admin.site.register(Tag, TagAdmin)
