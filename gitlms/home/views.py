from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from accounts.models import User
from lms.models import Institute,Department,Course
from lms.queryProxy import QueryCacheProxy

def home(request):
    if request.user.is_authenticated:
        return redirect('institutes')
    else:
        return redirect('welcome')



@login_required
def students(request):
    users=User.objects.all()
    context={'name':request.user.username,'users':users}

    return render(request,"pages/students.html",context)


@login_required
def appoint(request):
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
            rusers = User.objects.filter(role='user')
        
        except Institute.DoesNotExist:
            pass

    elif request.user.department != -1:
        try:
            department = Department.objects.get(id=request.user.department)
            course_ids = Course.objects.filter(department=department).values_list('id', flat=True)

            moderators = User.objects.filter(course__in=course_ids)
            rusers = User.objects.filter(role='user')
        
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

