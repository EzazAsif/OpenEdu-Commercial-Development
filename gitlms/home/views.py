from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from accounts.models import User
from lms.models import Institute,Department,Course
from lms.queryProxy import QueryCacheProxy
from django.core.cache import cache
import time

def home(request):
    user = request.user

    if not user.is_authenticated:
        return redirect('welcome')
    
    if not user.has_usable_password() or not all([user.username, user.first_name, user.last_name]):
        return redirect('completesignup')

    return redirect('institutes')



@login_required
def students(request):
    # Parameters for pagination (lazy loading)
    offset = int(request.GET.get('offset', 0))
    limit = 20  # number of users per batch

    cache_key = f'all_users_{offset}_{limit}'
    users = cache.get(cache_key)
    if not users:
        users = list(User.objects.all()[offset:offset + limit])
        cache.set(cache_key, users, timeout=60 * 15)

    context = {
        'users': users,
        'offset': offset,
        'limit': limit,
    }

    # Check if request is from htmx (partial)
    if request.headers.get('HX-Request'):
        return render(request, 'partials/user_list.html', context)

    # Normal full page render
    context['name'] = request.user.username
    return render(request, 'pages/students.html', context)



@login_required
def appoint(request):
    cache_key_base = 'regular_users'
    proxy = QueryCacheProxy(request.user)

    if request.user.role not in ['admin', 'master']:
        return redirect('/errors/unauthorizedaccess')

    # Default empty sets to avoid errors
    admins = User.objects.none()
    moderators = User.objects.none()
    rusers = []
    # Pagination parameters for rusers lazy loading
    offset = int(request.GET.get('offset', 0))
    limit = int(request.GET.get('limit', 20))  # default 1 per your case
    

    if request.user.institute != -1:
        try:
            institute = proxy._get_institute(request.user.institute)
            department_ids = Department.objects.filter(institute=institute).values_list('id', flat=True)
            course_ids = Course.objects.filter(department__in=department_ids).values_list('id', flat=True)

            admins = User.objects.filter(department__in=department_ids)
            moderators = User.objects.filter(course__in=course_ids)
            cache_key = f"{cache_key_base}_{offset}_{limit}"
            rusers = cache.get(cache_key)
            if rusers is None:
                print("No cache for rusers slice")
                rusers = list(User.objects.filter(role='user')[offset:offset + limit])
                cache.set(cache_key, rusers, timeout=60 * 15)
        
        except Institute.DoesNotExist:
            pass

    elif request.user.department != -1:
        try:
            department = Department.objects.get(id=request.user.department)
            course_ids = Course.objects.filter(department=department).values_list('id', flat=True)

            moderators = User.objects.filter(course__in=course_ids)
            cache_key = f"{cache_key_base}_{offset}_{limit}"
            rusers = cache.get(cache_key)
            if rusers is None:
                print("No cache for rusers slice")
                rusers = list(User.objects.filter(role='user')[offset:offset + limit])
                cache.set(cache_key, rusers, timeout=60 * 15)
        
        except Department.DoesNotExist:
            pass
    print()
    print(rusers,limit,offset)
    isMaster=request.user.role=='master'
    if(request.user.institute!=-1):
        instituteId=request.user.institute
    if(request.user.department!=-1):
        instituteId=Department.objects.get(id=request.user.department).institute.id
    if request.headers.get('HX-Request'):
        context = {
        'rusers': rusers,
        'offset': offset,
        'limit': limit,
    }
        
       
        return render(request, 'partials/rusers_list.html',context)
    context = {
    'instituteId': instituteId,
    'name': request.user.username,
    'rusers': rusers,
    'admins': admins,
    'moderators': moderators,
    'isMaster': isMaster,
    'offset': offset,
    'limit': limit,
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

