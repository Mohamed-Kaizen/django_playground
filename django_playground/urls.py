"""
django_playground URL Configuration
"""
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import TemplateView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenRefreshView
from dj_rest_auth.registration.views import VerifyEmailView
from .views import StaffGraphQLView

schema_view = get_schema_view(
    openapi.Info(
        title="Django PlayGround API",
        default_version="v1",
        description="Testing place for django apps",
        contact=openapi.Contact(email="m.n.kaizen@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=False,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = i18n_patterns(
    path("admin/", admin.site.urls),
    path("nested_admin/", include("nested_admin.urls")),
    path("graphql/", StaffGraphQLView.as_view(graphiql=True)),
    path(
        ".well-known/security.txt",
        TemplateView.as_view(template_name="security.txt", content_type="text/plain",),
    ),
    path(
        "robots.txt",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain",),
    ),
    path("api/users/", include("dj_rest_auth.urls")),
    path("api/users/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/users/register/", include("dj_rest_auth.registration.urls")),
    path('api/users/confirm-email/', VerifyEmailView.as_view(), name='account_email_verification_sent'),
    path("api/users/", include("users.urls")),
    path("api/blog/", include("blog.urls")),
    path("api/analytics/", include("analytics.urls")),
    path("api/learn/", include("e_learning.urls")),
    re_path(
        r"^docs(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "docs/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    prefix_default_language=False,
)

if settings.DEBUG:
    import debug_toolbar
    from django.conf.urls.static import static

    urlpatterns += [path("__debug__/", include(debug_toolbar.urls))] + static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
