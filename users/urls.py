from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="users/account/login.html"),
        name="account_login",
    ),
    path("signup/", views.accountSignup, name="account_signup"),
    path(
        "logout/",
        auth_views.LogoutView.as_view(template_name="users/account/logout.html"),
        name="account_logout",
    ),
    re_path(r"^profile/(?P<username>\w+)/$", views.profile, name="account_profile"),
    path(
        "user/password-reset/",
        auth_views.PasswordResetView.as_view(
            template_name="users/account/reset/password_reset.html"
        ),
        name="password_reset",
    ),
    path(
        "user/password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="users/account/reset/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "user/password-reset-confirm/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="users/account/reset/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "user/password-reset-complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="users/account/reset/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]
