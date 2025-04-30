from django.urls import path
from .views import *

urlpatterns = [path('', conferance_home, name='conferance_home'),
               path('conferance_start', conferance_start, name='conferance_start'),
               ]

