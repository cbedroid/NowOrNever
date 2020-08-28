from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('account/login/', auth_views.LoginView.as_view(template_name="users/snippets/account/login.html"), name='account_login'),
    path('account/logout/', auth_views.LogoutView.as_view(template_name="users/snippets/account/logout.html"), name='account_logout'),
    path('account/signup/', views.accountSignup, name="account_signup"),
    path('account/profile/', views.profile, name='profile'),

]



