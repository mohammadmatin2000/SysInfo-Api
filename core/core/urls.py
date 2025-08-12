from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
# ======================================================================================================================
schema_view = get_schema_view(
    openapi.Info(
        title="Flower Shop API",
        default_version="v1",
        description="مستندات API برای فروشگاه گل",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
# ======================================================================================================================
urlpatterns = [
    path('admin/', admin.site.urls),
    path('sysmonitor/',include("sysmonitor.urls")),

    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),

    # صفحه مستندات Redoc
    path(
        "redoc/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
]
# ======================================================================================================================
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# ======================================================================================================================