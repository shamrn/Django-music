from django.urls import path
from . import views


urlpatterns = [
    path('',views.SongListView.as_view(),name='song_list'),
]
