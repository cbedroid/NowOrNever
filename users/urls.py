from django.urls import path
from . import views

urlpatterns = [
    path('account/login/', views.accountLogin, name='account_login'),
    path('account/signup/', views.accountSignup, name="account_signup"),
    path("account/logout/", views.accountLogout, name="account_logout"),
    path('account/profile/', views.profile, name='profile'),

]



