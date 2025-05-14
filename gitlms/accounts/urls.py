from django.urls import path
from .views import *

urlpatterns = [
    path('', welcome, name='welcome'),
    path('welcome/', welcome, name='welcome'),
    path('login/', login, name='login'),
    path('signup/', signup, name='signup'),  # Already included
    path('logout/', logout_view, name='logout'),
    path('viewprofile/', view_profile, name='viewprofile'),
    path('editprofile/', edit_profile, name='editprofile'),
    path('settings/', settings_view, name='settings'),
    path('loginsessions/', login_sessions, name='loginsessions'),
    path('completelogin/',completesignup,name='completesignup'),
]
