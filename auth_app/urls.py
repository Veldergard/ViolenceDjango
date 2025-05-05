from django.urls import path

from auth_app import views

urlpatterns = [
    path("", views.index, name="index"),
    path('login/', views.login_page, name='login_page'),  # Login page
    path('register/', views.register_page, name='register_page'),  # Registration page
]
