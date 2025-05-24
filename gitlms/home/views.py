from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from accounts.models import User
from lms.models import Institute,Department,Course
from lms.queryProxy import QueryCacheProxy
from django.core.cache import cache
from elasticsearch_dsl import Q
from accounts.documents import UserDocument
from.queryfuncs import get_department_and_course_ids

def home(request):
    user = request.user

    if not user.is_authenticated:
        return redirect('welcome')
    
    if not user.has_usable_password() or not all([user.username, user.first_name, user.last_name]):
        return redirect('completesignup')

    return redirect('institutes')





@login_required
def students(request):
    offset = int(request.GET.get('offset', 0))
    limit = 20  # number of users per batch

    cache_key = f'all_users_{offset}_{limit}'
    users = cache.get(cache_key)

    if not users:
        # Elasticsearch query to get all users (assuming no filter needed)
        # If you want, you can add a filter query here (e.g. role='user' or active=True)
        search = UserDocument.search()[offset:offset + limit]

        users = []
        for hit in search:
            data = hit.to_dict()
            data['id'] = hit.meta.id
            users.append(data)

        cache.set(cache_key, users, timeout=60 * 15)

    context = {
        'users': users,
        'offset': offset,
        'limit': limit,
    }

    if request.headers.get('HX-Request'):
        return render(request, 'partials/user_list.html', context)

    context['name'] = request.user.username
    return render(request, 'pages/students.html', context)




@login_required
def appoint(request):
    cache_key_base = 'regular_users'
    proxy = QueryCacheProxy(request.user)

    if request.user.role not in ['admin', 'master']:
        return redirect('/errors/unauthorizedaccess')

    admins = User.objects.none()
    moderators = User.objects.none()
    rusers = []
    department_ids=[]
    course_ids=[]
    departmen
    offset = int(request.GET.get('offset', 0))
    limit = int(request.GET.get('limit', 20))

    try:
        if request.user.institute != -1:
            institute = proxy._get_institute(request.user.institute)
            department_ids,course_ids = get_department_and_course_ids(institute)
            
            

            # Elasticsearch queries for admins and moderators filtering by department and course ids
            q_admins = Q('terms', department=list(department_ids))
            q_mods = Q('terms', course=list(course_ids))

                # Fetch admins
            admins_search = UserDocument.search().query(q_admins)[:100]  # adjust size as needed
            admins = [hit.to_dict() for hit in admins_search]

            # Fetch moderators
            moderators_search = UserDocument.search().query(q_mods)[:100]
            moderators = [hit.to_dict() for hit in moderators_search]

        elif request.user.department != -1:
            department = Department.objects.get(id=request.user.department)
            course_ids = Course.objects.filter(department=department).values_list('id', flat=True)

            q_mods = Q('terms', course=list(course_ids))
            moderators_search = UserDocument.search().query(q_mods)[:100]
            moderators = [hit.to_dict() for hit in moderators_search]

    except (Institute.DoesNotExist, Department.DoesNotExist):
        pass

    # Compose Elasticsearch query to filter role='user'
    q = Q('term', role='user')
    
    # Search query with pagination
    cache_key = f"{cache_key_base}_{offset}_{limit}"
    rusers = cache.get(cache_key)
    if rusers is None:
        # Run the Elasticsearch query
        search = UserDocument.search().query(q)[offset:offset+limit]
        rusers = []
        for hit in search:
            data = hit.to_dict()
            data['id'] = hit.meta.id
            rusers.append(data)
        cache.set(cache_key, rusers, timeout=60 * 15)

    isMaster = request.user.role == 'master'

    instituteId = None
    if request.user.department != -1:
        try:
            instituteId = Department.objects.get(id=request.user.department).institute.id
        except Department.DoesNotExist:
            pass
    elif request.user.institute != -1:
        instituteId = request.user.institute

    if request.headers.get('HX-Request'):
        context = {
            'rusers': rusers,
            'offset': offset,
            'limit': limit,
        }
        return render(request, 'partials/rusers_list.html', context)

    context = {
        'instituteId': instituteId,
        'name': request.user.username,
        'rusers': rusers,
        'admins': admins,
        'moderators': moderators,
        'isMaster': isMaster,
        'offset': offset,
        'limit': limit,
        'departments':department_ids,
        'courses':course_ids,
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

