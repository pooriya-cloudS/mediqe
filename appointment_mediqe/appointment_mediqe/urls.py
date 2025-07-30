from django.contrib import admin
from django.urls import path, include
from . import settings
from django.conf.urls.static import static

urlpatterns = [
    path("api-auth/", include("rest_framework.urls")),
    path("admin/", admin.site.urls),
    path("api/", include("appointments.api.v1.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
