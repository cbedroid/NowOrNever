from django.urls import path, re_path
from . import views

app_name = "core"
urlpatterns = [
    re_path(r"contact_us/$(?i)", views.contactUs, name="contact_us"),
    re_path(
        r"terms-policy/privacy_policy/$(?i)", views.privacyPolicy, name="privacy_policy"
    ),
    #path("video/<video_id>/", views.VideoRatingDetailView.as_view(),name="core_video"),
]
