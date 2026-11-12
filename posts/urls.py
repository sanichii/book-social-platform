from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.feed_view, name='feed'),
    path('<int:pk>/like/', views.toggle_like, name='toggle_like'),
    path('<int:pk>/comment/', views.add_comment, name='add_comment'),
    path('<int:pk>/delete/', views.delete_post, name='delete_post'),
]