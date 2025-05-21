from django.urls import path
from . import views

urlpatterns = [
    path('', views.video_input_view, name='video_input'),
    path('video_feed/', views.video_feed, name='video_feed'),
]
