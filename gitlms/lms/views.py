
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import Department,Course,Faculty,Slide,Video,Note,Institute
from django.conf import settings
from .contentViewers import *
from .queryProxy import QueryCacheProxy


@login_required
def institutes(request):
    user=request.user
    if not user.has_usable_password() or not all([user.username, user.first_name, user.last_name]):
        return redirect('completesignup')
    institutes_proxy = QueryCacheProxy(request.user)
    institutes = institutes_proxy.get_institutes()  # Fetch departments via the proxy
    # Determine the visibility of the modal and button based on the user's role
    context={
        'institutes':institutes,
     
        
    }

    # Render the departments page with the context
    return render(request, "lms/institutions.html", context)


@login_required
def departments(request,ins_id):
    department_proxy = QueryCacheProxy(request.user)
    departments,institute = department_proxy.get_departments(ins_id)  # Fetch departments via the proxy
    
    # Determine the visibility of the modal and button based on the user's role
    showDeptModal = (request.user.institute == ins_id)
    showUpdateDeptModal = (request.user.institute == ins_id)
    showAddButton = (request.user.institute == ins_id)
    
    # Prepare the context with user and departments information
    context = {
        'institute':institute,
        'name': request.user.username,
        'departments': departments,
        'showDeptModal': showDeptModal,
        'showUpdateDeptModal': showUpdateDeptModal,
        'showAddButton': showAddButton
    }

    # Render the departments page with the context
    return render(request, "lms/departments.html", context)

@login_required
def courses(request):
    courses = Course.objects.all().order_by('course_name')

    context={'name':request.user.username,'courses':courses}

    return render(request,"courses.html",context)

# Create your views here.

#for Courses inside a Department
@login_required
def deptcourses(request,ins_id,id):
    course_proxy = QueryCacheProxy(request.user)
    
    courses,department,institute = course_proxy.get_deptCourses(ins_id,id)  # Fetch departments via the pr
    showAddButton=(request.user.institute==ins_id)or(request.user.department==department.id)
    showUpdateCourseModal=(request.user.institute==ins_id)or(request.user.department==department.id)
    showCourseModal=(request.user.institute==ins_id)or(request.user.department==department.id)
    context={'name':request.user.username,'courses':courses , 'department': department,'institute':institute,
             'showCourseModal':showCourseModal,'showUpdateCourseModal':showUpdateCourseModal,'showAddButton':showAddButton}
    return render(request,'lms/deptcourses.html',context)




#for faculties inside a Course
@login_required
def course_facs(request, ins_id,dept_id, course_id):
    faculty_proxy = QueryCacheProxy(request.user)
    faculties,course,department,institute = faculty_proxy.get_courseFacs(ins_id,dept_id,course_id)
    showFacultyModal=(request.user.institute==ins_id)or(request.user.department==department.id)or(request.user.course==course.id)
    showUpdateFacultyModal=(request.user.institute==ins_id)or(request.user.department==department.id)or(request.user.course==course.id)
    showAddButton=(request.user.institute==ins_id)or(request.user.department==department.id)or(request.user.course==course.id)
    context = {'institute':institute,'department': department, 'faculties': faculties,'course':course,
               'showFacultyModal':showFacultyModal,'showUpdateFacultyModal':showUpdateFacultyModal,'showAddButton':showAddButton}
    return render(request, 'lms/faculty.html', context)



#for lectures inside a Faculty
@login_required
def fac_lecs(request, ins_id,dept_id, course_id,fac_id):
    lecture_proxy=QueryCacheProxy(request.user)
    faculty,course,department,institute = lecture_proxy._get_faculty(ins_id,dept_id,course_id,fac_id)
    context = {'institute':institute,'department': department, 'faculty': faculty,'course':course,'MEDIA_URL':settings.MEDIA_URL}
    return render(request, 'lms/lectures.html', context)

#for slides inside a lecture
@login_required
def lec_slides(request,ins_id,dept_id, course_id,fac_id):
    slide_proxy = QueryCacheProxy(request.user)
    slides,faculty,course,department,institute = slide_proxy.get_LecSlides(ins_id,dept_id,course_id,fac_id)
    
    
    context = {'institute':institute,'department': department, 'faculty': faculty ,'course':course,'slides':slides,'showSlideModal':True,'showUpdateSlideModal':True,'showAddButton':True}
    
    return render(request,"lms/slides.html",context)



# For videos inside a lecture
@login_required
def lec_videos(request, ins_id,dept_id, course_id, fac_id):
    video_proxy = QueryCacheProxy(request.user)
    videos,faculty,course,department,institute = video_proxy.get_LecVideos(ins_id,dept_id,course_id,fac_id)
    context = {'institute':institute,'department': department, 'faculty': faculty, 'course': course, 'videos': videos,'showVideoModal':True,'showUpdateVideoModal':True,'showAddButton':True}
    return render(request, "lms/videos.html", context)



# For notes inside a lecture
@login_required
def lec_notes(request,ins_id, dept_id, course_id, fac_id):
    note_proxy = QueryCacheProxy(request.user)
    notes,faculty,course,department,institute = note_proxy.get_LecNotes(ins_id,dept_id,course_id,fac_id)
    context = {'institute':institute,'department': department, 'faculty': faculty, 'course': course, 'notes': notes,'showNoteModal':True,'showUpdateNoteModal':True,'showAddButton':True}
    return render(request, "lms/notes.html", context)

