from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from accounts.models import User
from lms.models import Institute,Department,Course
from lms.queryProxy import QueryCacheProxy
from django.core.cache import cache


def home(request):
    user = request.user

    if not user.is_authenticated:
        return redirect('welcome')
    
    if not user.has_usable_password() or not all([user.username, user.first_name, user.last_name]):
        return redirect('completesignup')

    return redirect('institutes')

@login_required
def students(request):
    cache_key = 'all_users'
    users=cache.get(cache_key)
    if not users:
       users=User.objects.all()
       cache.set(cache_key, users, timeout=60*15)  # Cache for 15 minutes
    context={'name':request.user.username,'users':users}

    return render(request,"pages/students.html",context)


@login_required
def appoint(request):
    cache_key = 'regular_users'
    proxy = QueryCacheProxy(request.user)

    if request.user.role not in ['admin', 'master']:
        return redirect('/errors/unauthorizedaccess')

    # Default empty sets to avoid errors
    admins = User.objects.none()
    moderators = User.objects.none()
    rusers = User.objects.none()

    if request.user.institute != -1:
        try:
            institute = proxy._get_institute(request.user.institute)
            department_ids = Department.objects.filter(institute=institute).values_list('id', flat=True)
            course_ids = Course.objects.filter(department__in=department_ids).values_list('id', flat=True)

            admins = User.objects.filter(department__in=department_ids)
            moderators = User.objects.filter(course__in=course_ids)
            rusers = cache.get(cache_key)
            if rusers is None:
                print("No cache")
                rusers = list(User.objects.filter(role='user'))  # Convert to list before caching
                cache.set(cache_key, rusers, timeout=60*15)  # Cache for 15 minutes
            else:
                print("using cache")
        
        except Institute.DoesNotExist:
            pass

    elif request.user.department != -1:
        try:
            department = Department.objects.get(id=request.user.department)
            course_ids = Course.objects.filter(department=department).values_list('id', flat=True)

            moderators = User.objects.filter(course__in=course_ids)
            rusers = cache.get(cache_key)

            if rusers is None:
                print("No cache")
                rusers = list(User.objects.filter(role='user'))  # Convert to list before caching
                cache.set(cache_key, rusers, timeout=60*15)  # Cache for 15 minutes
            else:
                print("using cache")
        
        except Department.DoesNotExist:
            pass
    
    isMaster=request.user.role=='master'
    if(request.user.institute!=-1):
        instituteId=request.user.institute
    if(request.user.department!=-1):
        instituteId=Department.objects.get(id=request.user.department).institute.id
    context = {
        'instituteId':instituteId,
        'name': request.user.username,
        'rusers': rusers,
        'admins': admins,
        'moderators': moderators,
        'isMaster':isMaster
    }

    return render(request, "pages/appoint.html", context)



@login_required
def changerole(request,userid,role):
    if(request.user.role not in ['admin','master']):
        return redirect('/errors/illegalactivity')
        
    if((role=='master' or role=='admin')and request.user.role!='master'):
        return redirect('/errors/illegalactivity')
    user=User.objects.get(id=userid)
    user.role=role
    user.save()
    return redirect('appoint')

