"""NoworNever URL Configuration"""

from django.urls import include, re_path
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin

if settings.DEBUG:
    ADMIN_URL = re_path(r"^admin/", admin.site.urls)
else:
    ADMIN_URL = re_path(r"^non/spud/admin/$", admin.site.urls)
 

urlpatterns = [
    re_path(r"^nowornever/", include("core.urls")),
    re_path(r"^account/", include("users.urls.account_urls")),
    ADMIN_URL,
    re_path(r"^user/", include("users.urls.users_urls")),
   re_path("", include("countrycuzzins.urls")),
]


#Amin Custom Site Title
admin.site.site_header = "NoworNever"
admin.site.site_title = "NoworNever Admin Portal"
admin.site.index_title = "Welcome to NoworNever Entertainment Portal"

# Production and Development Admin
handler404 = "users.views.error_404"

media_url = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
static_url = static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += media_url
urlpatterns += static_url
