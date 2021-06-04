from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('',views.service,name='service'),
    path('login/',views.login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('profile_update/',views.profile_update,name='profile_update'),
]
