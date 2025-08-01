from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.api_urls')),  # 👈 این الان کار می‌کنه
    path('accounts/', include('accounts.urls')),  # برای ورود/خروج و سایر URLها
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
