from django.urls import path
from django.views.generic import TemplateView

from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.service, name='service'),

    path('login', TemplateView.as_view(template_name='service/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('profile_update/', views.ProfileUpdateViews.as_view(), name='profile_update'),
    path('inventory_update/', views.inventory_update, name='inventory_update'),
    path('song_create/', views.SongCreateView.as_view(), name='song_create'),
    path('song_update/<pk>/', views.SongUpdateView.as_view(), name='song_update'),
    path('song_delete/<pk>/', views.song_delete, name='song_delete'),
]
