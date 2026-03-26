from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import TemplateView
from django.views.static import serve
from django.conf import settings
import os

artifacts_root = str(settings.ARTIFACTS_DIR)
assets_root = str(settings.REACT_BUILD_DIR / 'assets')

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("polls.urls")),
]

# Always serve artifacts and assets (kiosk app — no separate web server).
urlpatterns += [
    re_path(r'^artifacts/(?P<path>.*)$', serve, {'document_root': artifacts_root}),
    re_path(r'^assets/(?P<path>.*)$', serve, {'document_root': assets_root}),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Catch-all: serve the React SPA for any non-API route.
urlpatterns += [
    re_path(r'^.*$', TemplateView.as_view(template_name='index.html')),
]
