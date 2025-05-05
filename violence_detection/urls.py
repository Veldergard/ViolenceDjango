"""
URL configuration for violence_detection project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings  # Application settings
from django.contrib import admin  # Django admin module
from django.contrib.staticfiles.urls import staticfiles_urlpatterns, static  # Static files serving
from django.urls import include
from django.urls import path  # URL routing

urlpatterns = [
    path('auth/', include('auth_app.urls')),
    path('polls/', include('polls_app.urls')),
    path('video/', include('video_app.urls')),
    path('admin/', admin.site.urls),
]

# Serve media files if DEBUG is True (development mode)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Serve static files using staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()