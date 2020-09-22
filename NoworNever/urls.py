"""NoworNever URL Configuration"""

from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings
import countrycuzzins as cc

urlpatterns = [
    path("", include("countrycuzzins.urls")),
    path("", include("users.urls")),
]

# Production and Development Admin
if settings.DEBUG == True:
    urlpatterns.append(path("admin/", admin.site.urls))
else:
    urlpatterns.append(path("Non/Spud/admin/", admin.site.urls))


handler404 = "users.views.error_404"
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
