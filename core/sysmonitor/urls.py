from django.urls import path
from .views import SystemInfoView, SystemStatusView
# ======================================================================================================================
urlpatterns = [
    path('info/', SystemInfoView.as_view(), name='system_info'),
    path('status/', SystemStatusView.as_view(), name='system_status'),
]
# ======================================================================================================================