from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('article/<slug:slug>/', views.ArticleDetailView.as_view(), name='article-detail'),
    path('countrycuzzins/album/<slug:slug>/', views.AlbumList.as_view(), name='albums'),
    path('account/login/', views.accountLogin, name='account_login'),
    path('account/signup/', views.accountSignup, name="account_signup"),
    path("account/logout", views.accountLogout, name="account_logout"),

]

#TESTING VIEW ONLY -- CAN DELETE WHEN DONE
testing = [
    path('testing/', views.test_html, name='testing'),
  path('music/',views.test_music_player,name='musicplayer')

]

urlpatterns.extend(testing)


