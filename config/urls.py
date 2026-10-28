from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include(("contact.auth_urls", "accounts"), namespace="accounts")),
    path("contact/", include("contact.urls")),
    path("payments/", include("payments.urls")),
    path("health/", TemplateView.as_view(template_name="health.html"), name="health"),
    path("", TemplateView.as_view(template_name="index.html"), name="home"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
