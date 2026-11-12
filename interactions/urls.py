from django.urls import path
from . import views

app_name = 'interactions'

urlpatterns = [
    path('readers/', views.readers_list, name='readers_list'),
    path('profile/<str:username>/', views.user_public_profile, name='user_profile'),
    path('follow/<str:username>/', views.toggle_follow, name='toggle_follow'),
]