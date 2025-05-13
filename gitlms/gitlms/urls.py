"""
URL configuration for gitlms project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('lms/', include('lms.urls')),
    path('', include('home.urls')),
    path('errors/', include('errors.urls')),
    path('notifications/', include('notifications.urls')),
    path('chat/', include('commChat.urls')),
    path('classroom/', include('videomeet.urls')),
    path('auth/', include('allauth.urls')),  # This includes allauth URLs under '/auth/'

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

