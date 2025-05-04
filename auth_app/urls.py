from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns, static  # Static files serving
from django.urls import path

from auth_app import views

urlpatterns = [
    path("", views.index, name="index"),
    path('login/', views.login_page, name='login_page'),  # Login page
    path('register/', views.register_page, name='register_page'),  # Registration page
]

# Serve media files if DEBUG is True (development mode)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Serve static files using staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()
