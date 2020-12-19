"""NoworNever URL Configuration"""

from django.contrib import admin
from django.urls import include, path, re_path
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("nowornever/", include("core.urls")),
    path("", include("countrycuzzins.urls")),
    #path("countrycuzzins/", include("countrycuzzins.urls")),
    path("user/", include("users.urls.users_urls")),
    path("account/", include("users.urls.account_urls")),
]


#Amin Custom Site Title
admin.site.site_header = "NoworNever"
admin.site.site_title = "NoworNever Admin Portal"
admin.site.index_title = "Welcome to NoworNever Entertainment Portal"

# Production and Development Admin
if settings.DEBUG == True:
    urlpatterns.append(path("admin/", admin.site.urls))
else:
    urlpatterns.append(path("Non/Spud/admin/", admin.site.urls))

handler404 = "users.views.error_404"

media_url = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
static_url = static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += media_url
urlpatterns += static_url
