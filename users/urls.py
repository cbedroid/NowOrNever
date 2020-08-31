from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('account/login/', auth_views.LoginView.as_view(template_name="users/account/login.html"), name='account_login'),
    path('account/signup/', views.accountSignup, name="account_signup"),
    path('account/logout/', auth_views.LogoutView.as_view(template_name="users/account/logout.html"), name='account_logout'),
    path('account/profile/', views.profile, name='account_profile'),

]



