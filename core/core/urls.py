from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

# ======================================================================================================================
# تنظیمات Swagger / OpenAPI برای مستندات API
# ======================================================================================================================
schema_view = get_schema_view(
    openapi.Info(
        title="Flower Shop API",          # عنوان پروژه API
        default_version="v1",             # نسخه پیش‌فرض
        description="مستندات API برای فروشگاه گل",  # توضیحات پروژه
    ),
    public=True,                          # مستندات برای همه در دسترس باشد
    permission_classes=(permissions.AllowAny,),  # اجازه دسترسی عمومی
)

# ======================================================================================================================
# URL های اصلی پروژه
# ======================================================================================================================
urlpatterns = [
    # پنل ادمین
    path('admin/', admin.site.urls),

    # مسیر اپ sysmonitor
    path('sysmonitor/', include("sysmonitor.urls")),

    # مسیر Swagger UI برای مستندات API
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),

    # مسیر Redoc UI برای مستندات API
    path(
        "redoc/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
]

# ======================================================================================================================
# اضافه کردن مسیر فایل‌های استاتیک و مدیا در حالت توسعه
# ======================================================================================================================
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# ======================================================================================================================