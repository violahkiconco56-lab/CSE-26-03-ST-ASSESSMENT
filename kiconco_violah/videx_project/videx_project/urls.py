"""
URL configuration for videx_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from videx import views

urlpatterns = [
   path('admin/', admin.site.urls),
   path('', views.index, name='index'),
   path('upload/', views.upload_video, name='upload_video'),
   path('videos/', views.video_list, name='video_list'),# list of videos
   path('video/<int:pk>/', views.video_detail, name='video_detail'),# single video
   path('video/<int:pk>/delete/', views.delete_video, name='delete_video'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
