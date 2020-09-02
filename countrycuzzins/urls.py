from django.urls import path,re_path
from . import views

urlpatterns = [
    path('', views.index, name="home"),
    #re_path(r'(?:\(countrycuzzins/home|home\)/)?', views.index, name="home"),
    path('article/<slug:slug>/', views.ArticleDetailView.as_view(), name='article-detail'),
    path('countrycuzzins/album/<slug:slug>/', views.AlbumList.as_view(), name='albums'),
    path('countrycuzzins/events/', views.EventList.as_view(), name='events'),

]

#TESTING VIEW ONLY -- CAN DELETE WHEN DONE
testing = [
    path('testing/', views.test_html, name='testing'),
  path('music/',views.test_music_player,name='musicplayer')

]

urlpatterns.extend(testing)


