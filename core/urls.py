from django.urls import path, re_path
from . import views

urlpatterns = [
    re_path(r"contact_us/$(?i)", views.contactUs, name="contact_us"),
    re_path(r"terms-policy/privacy_policy/$(?i)",
            views.privacyPolicy, name="privacy_policy"),
]
