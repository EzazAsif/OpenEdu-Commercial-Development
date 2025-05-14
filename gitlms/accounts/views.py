from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import User
from .accountfuncs import checkvalidity
from .decorators import log_activity
from .observers import UserProfileUpdatedObserver
from .facade import RegistrationFacade
# from .observers import SessionLogger, SessionAnalytics
from .factory import SessionDisplayFactory 
from django.contrib.sessions.models import Session
from django.utils import timezone





@log_activity  # Apply the decorator to log activity for login
def login(request):
    if request.method == "POST":
        data = request.POST
        email = data.get('email')
        password = data.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "User does not exist")
            return redirect('/accounts/login/')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            auth_login(request, user)
            messages.success(request, "Successfully logged in")
            return redirect('/')
        else:
            messages.error(request, "Invalid password")
            return redirect('/accounts/login/')
    
    return render(request, "login.html")


@log_activity  # Apply the decorator to log activity for signup
def signup(request):
    if request.method == "POST":
        data = request.POST
        Firstname = data.get('fname')
        Lastname = data.get('lname')
        Email = data.get('email')
        password = data.get('passw')
        rpassword = data.get('rpassw')
        username = f"{Firstname}_{Lastname}"

        if checkvalidity(request, passw=password, rpassw=rpassword, username=username, email=Email):
            registration_facade = RegistrationFacade()  # Use the facade for registration
            user = registration_facade.register(data)  # Call the facade's register method
        # Here you can associate the SocialAccount with the user
            messages.success(request, "Registration successful. You can now log in.")

            return redirect('/accounts/login/')
        
    return render(request, "registration.html")


@login_required
@log_activity  # Apply the decorator to log activity for profile editing
def edit_profile(request):
    user = request.user
    if request.method == "POST":
        data = request.POST
        Firstname = data.get('FirstName')
        Lastname = data.get('LastName')
        Email = data.get('email')
        password = data.get('psw')
        rpassword = data.get('psw-repeat')
        picture = request.FILES.get('editpp')
        print(picture)

        if password and rpassword:
            if password == rpassword:
                user.set_password(password)
            else:
                messages.error(request, "Passwords don't match")

        if Firstname:
            user.first_name = Firstname
        if Lastname:
            user.last_name = Lastname
        if Email:
            user.email = Email
            user.username=Email
        if picture:
            user.profilepicture = picture

        user.save()
        
        # Notify observers about the profile update
        observer = UserProfileUpdatedObserver()
        observer.update(request,user)

        return redirect('/')
    
    return render(request, "editprofile.html", context={'users': user})


@log_activity  # Apply the decorator to log activity for logout
def logout_view(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('login')



# Views
def welcome(request):
    return render(request, "welcome.html")

@login_required
def view_profile(request):
    user = request.user
    
    context = {
        'user': user,
        'full_name': user.get_full_name() if user.get_full_name() else user.username,
        'email': user.email,
        'role': user.role,
        'profile_picture': user.profilepicture.url if user.profilepicture else 'https://via.placeholder.com/150'
    }
    
    return render(request, 'viewprofile.html', context)

@login_required
def settings_view(request):
    return render(request, 'settings.html')

@login_required
def login_sessions(request):
    active_sessions = []
    for session in Session.objects.filter(expire_date__gte=timezone.now()):
        session_data = session.get_decoded()
        if str(request.user.id) == session_data.get('_auth_user_id'):
            # Create display data
            display = SessionDisplayFactory.create_display('detailed', session, request)
            session_info = display.get_display_data()
            active_sessions.append(session_info)
    
    return render(request, 'loginsessions.html', {
        'active_sessions': sorted(active_sessions, key=lambda x: x['last_activity'], reverse=True)
    })


@login_required
@log_activity  # Apply the decorator to log activity for profile editing
def completesignup(request):
    user = request.user
    if request.method == "POST":
        data = request.POST
        Firstname = data.get('FirstName')
        Lastname = data.get('LastName')
        password = data.get('psw')
        rpassword = data.get('psw-repeat')
        picture = request.FILES.get('editpp')
        if user.username != user.email:
           user.username=user.email    
        if password and rpassword:
            if (password != rpassword):
               messages.error(request, "Passwords don't match")
            elif len(password)<8:
                messages.error(request, "Passwords length too small")
            else:
                user.set_password(password)

        if Firstname:
            user.first_name = Firstname
        if Lastname:
            user.last_name = Lastname
        
          
        if picture:
            user.profilepicture = picture

        user.save()
        
        # Notify observers about the profile update
        observer = UserProfileUpdatedObserver()
        observer.update(request,user)

        return redirect('institutes')
    
    return render(request, "logincompletion.html", context={'users': user})
