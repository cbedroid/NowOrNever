from .base_urls import *

app_name="users"
urlpatterns = [
    re_path(r"^profile/", views.profile, name="user-profile"),
    re_path(r"^profile/(?P<user>.*)/$", views.profile, name="user-profile"),
]
    