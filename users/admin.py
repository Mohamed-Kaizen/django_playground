from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from import_export import resources
from import_export.admin import ExportActionModelAdmin

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import CustomUser


class UserResource(resources.ModelResource):
    class Meta:
        model = CustomUser
        fields = ("username", "email")

        export_order = ("username", "email")


class CustomUserAdmin(ExportActionModelAdmin, UserAdmin):
    """
    Configure the users app in admin app
    """

    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    resource_class = UserResource
    model = CustomUser
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "password1",
                    "password2",
                    "full_name",
                    "picture",
                ),
            },
        ),
        (_("Permissions"), {"fields": ("is_superuser", "is_staff")}),
    )

    fieldsets = (
        (None, {"fields": ("username", "password", "user_uuid")}),
        (
            _("Personal info"),
            {"classes": ("collapse",), "fields": ("full_name", "email", "picture",)},
        ),
        (
            _("Permissions"),
            {
                "classes": ("collapse",),
                "fields": (
                    "is_active",
                    "is_superuser",
                    "is_staff",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (
            _("Important dates"),
            {"classes": ("collapse",), "fields": ("last_login", "date_joined")},
        ),
    )

    list_display = (
        "username",
        "email",
        "full_name",
        "is_active",
        "is_staff",
    )
    readonly_fields = ("user_uuid",)


admin.site.site_title = _("Django PlayGround site admin")
admin.site.site_header = _("Django PlayGround Dashboard")
admin.site.index_title = _("Welcome to Django PlayGround")
admin.site.register(CustomUser, CustomUserAdmin)
