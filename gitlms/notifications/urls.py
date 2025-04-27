from django.urls import path
from .views import *

urlpatterns = [
    
    path('', notifications, name='notifications'),
    path('2', notifications2, name='notifications2'),
    path('approve/<int:not_id>', approve_not, name='approve_not'),
    path('reject/<int:not_id>', reject_not, name='reject_not'),
    path('view/<int:not_id>',view_not,name='view_not'),
]
