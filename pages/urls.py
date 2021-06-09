from django.urls import path
from . import views

urlpatterns = [
    path('', views.SongListView.as_view(), name='song_list'),
    path('<get_param>/', views.SongListView.as_view(), name='song_list'),
    path('like/<actions>/<pk>/', views.like_song, name='like'),
    path('song/<slug>/', views.song_detail, name='song_detail'),
    path('author/<pk>/', views.author_detail, name='author_detail'),
]
