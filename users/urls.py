from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('account/login/', auth_views.LoginView.as_view(template_name="users/account/login.html"), name='account_login'),
    path('account/signup/', views.accountSignup, name="account_signup"),
    path('account/logout/', auth_views.LogoutView.as_view(template_name="users/account/logout.html"), name='account_logout'),
    path('account/profile/', views.profile, name='account_profile'),
    path('account/password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='users/account/reset/password_reset.html'),
         name='password_reset'),
    path('account/password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
              template_name='users/account/reset/password_reset_done.html'),
         name='password_reset_done'),
    path('account/password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='users/account/reset/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('account/password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='users/account/reset/password_reset_complete.html'),
         name='password_reset_complete'),
]



