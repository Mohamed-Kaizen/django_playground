from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _

from .signal import analytic_signal


class Analytic(models.Model):

    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        verbose_name=_("user"),
        on_delete=models.CASCADE,
        related_name="user_analysis",
        db_index=True,
    )

    content_type = models.ForeignKey(
        ContentType,
        verbose_name=_("content_type"),
        on_delete=models.DO_NOTHING,
        related_name="content_type_analysis",
        db_index=True,
    )

    object_id = models.PositiveIntegerField(verbose_name=_("object_id"))

    content_object = GenericForeignKey("content_type", "object_id")

    action = models.CharField(verbose_name=_("action"), max_length=10)

    device = models.TextField(verbose_name=_("device"))

    language = models.CharField(verbose_name=_("language"), max_length=100)

    created_at = models.DateTimeField(verbose_name=_("created_at"), auto_now_add=True)

    class Meta:

        verbose_name = _("analytic")

        verbose_name_plural = _("analytics")

    def __str__(self):
        return f"{self.user}-- {self.created_at}"


def analytic_receiver(sender, instance, request, *args, **kwargs):
    content_type = ContentType.objects.get_for_model(sender)
    Analytic.objects.create(
        user=request.user,
        content_type=content_type,
        object_id=instance.id,
        action=request.method,
        device=request.headers.get("User-Agent"),
        language=request.headers.get("Accept-Language"),
    )


analytic_signal.connect(analytic_receiver)
