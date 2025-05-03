from django.urls import path
from .views import *



urlpatterns = [
    path('<int:ins_id>', commChat, name='commChat'),
]
