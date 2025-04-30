from django.shortcuts import render
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from accounts.models import User

# Create your views here.
@login_required
def conferance_home(request):
    return render(request,"conferanceHome.html")

# Create your views here.
@login_required
def conferance_start(request):
    return render(request,"ConferanceStartPage.html")