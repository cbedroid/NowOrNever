"""NoworNever URL Configuration"""

from django.contrib import admin
from django.urls import include, path, re_path
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("nowornever/", include("core.urls")),
    path("NoworNever/", include("core.urls")),
    path("countrycuzzins/", include("countrycuzzins.urls")),
    path("account/", include("users.urls")),
]

# Production and Development Admin
if settings.DEBUG == True:
    urlpatterns.append(path("admin/", admin.site.urls))
else:
    urlpatterns.append(path("Non/Spud/admin/", admin.site.urls))


handler404 = "users.views.error_404"
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
