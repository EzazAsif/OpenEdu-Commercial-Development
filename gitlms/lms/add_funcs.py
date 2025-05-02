from django.shortcuts import render, redirect,get_object_or_404
from .models import *
from accounts.models import User
from django.http import HttpResponse
from django.contrib import messages
from .Observer import Subject ,MessageObserver
from notifications.models import Notification
from django.db.models import Q
from .contentFactory import *
from django.contrib.auth.decorators import login_required
from .queryProxy import QueryCacheProxy

messageObserver=MessageObserver()
subject=Subject()
subject.attach(messageObserver)

# Add Department
@login_required
def add_dept(request,ins_id):
    if (request.user.institute!=ins_id):
        return redirect('illegalactivity')
    proxy=QueryCacheProxy(request.user)
    Institute=proxy._get_institute(ins_id)
    if request.method == 'POST':
        dept_name = request.POST.get('departmentName')
        dept_desc = request.POST.get('departmentDescription')
        dept_image = request.FILES.get('departmentImage')
        if(dept_name  ):
            department=Department.objects.create( name=dept_name , institute= Institute)
            if(dept_image):
                department.image=dept_image
            if( dept_desc):
                department.description=dept_desc
        department.save()
        proxy=QueryCacheProxy(request.user)
        proxy.delete_departments_cache(ins_id)
        subject.notify(request, "Department has been added")
        return redirect('departments',ins_id)
    
    return redirect('departments',ins_id)

# Add Course
@login_required
def add_course(request,ins_id, dept_id):
    if (request.user.institute!=ins_id)and(request.user.department!= dept_id):
        return redirect('illegalactivity')
    department=get_object_or_404(Department,id=dept_id)
    if request.method == 'POST':
        course_code = request.POST.get('courseCode')
        course_name = request.POST.get('courseName')
        course_desc = request.POST.get('courseDescription')
        course_image = request.FILES.get('courseImage')
        if(course_code and course_name):
            course=Course.objects.create(course_code=course_code, course_name=course_name,department=department)
            if course_desc:
                course.description=course_desc
            if course_image:
                course.image=course_image
        course.save()
        proxy=QueryCacheProxy(request.user)
        proxy.delete_deptCourses_cache(ins_id, dept_id)
        subject.notify(request, "Course has been added")
    return redirect('deptcourses',ins_id, dept_id)



# Add Faculty
@login_required
def add_fac(request,ins_id, dept_id, course_id):
    if (request.user.institute!=ins_id)and(request.user.department!= dept_id)and(request.user.course!= course_id):
        return redirect('illegalactivity')
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        faculty_name = request.POST.get('facultyName')
        position = request.POST.get('position')
        image= request.FILES.get('facultyImage')
        if(faculty_name and position):
            faculty=Faculty.objects.create(name=faculty_name, position=position,course=course)
            if image:
                faculty.image=image
            faculty.save()
            proxy=QueryCacheProxy(request.user)
            proxy.delete_courseFacs_cache(ins_id, dept_id, course_id)
        subject.notify(request, "Faculty has been added")
    return redirect('course_facs',ins_id, dept_id, course_id)
    
 
# Add Slide
@login_required
def add_slide(request,ins_id, dept_id, course_id, fac_id):
    faculty = get_object_or_404(Faculty, id=fac_id)
    if request.method == 'POST':
        slide_name = request.POST.get('slideName')
        slide_content = request.FILES.get('slideContent')
        if (request.user.institute==ins_id) or (request.user.department == dept_id) or (request.user.course == course_id):
            SlideFactory.create_content(faculty, slide_name, slide_content)
            proxy=QueryCacheProxy(request.user)
            proxy.delete_LecSlides_cache(ins_id, dept_id, course_id, fac_id)
            subject.notify(request, "Slide has been added")
        else:
            temp_slide=TemporarySlideFactory.create_temp_content(real_instance=None, faculty=faculty, name=slide_name, content_file=slide_content)
            notification = Notification.objects.create(
                message=f"{request.user.first_name} {request.user.last_name} wants to add a slide in {temp_slide.faculty.course.department.name}/{temp_slide.faculty.course.course_name}/{temp_slide.faculty.name}",
                sender=request.user,
                type="add",
                content_type="slide",
                content_id=temp_slide.id
            )
            receivers = User.objects.filter(Q(role='master') | Q(department=dept_id) | Q(course=course_id))
            print(receivers)
            notification.recievers.add(*receivers)
            notification.save()
            subject.notify(request, "Request sent")
    return redirect('lec_slides', ins_id, dept_id, course_id, fac_id)
# Add Note
@login_required
def add_note(request,ins_id, dept_id, course_id, fac_id):
    faculty = get_object_or_404(Faculty, id=fac_id)
    if request.method == 'POST':
        note_name = request.POST.get('noteName')
        note_content = request.FILES.get('noteContent')
        if (request.user.institute==ins_id) or (request.user.department == dept_id) or (request.user.course == course_id):
            NoteFactory.create_content( faculty, note_name, note_content)
            proxy=QueryCacheProxy(request.user)
            proxy.delete_LecNotes_cache(ins_id, dept_id, course_id, fac_id)
            subject.notify(request, "Note has been added")
        else:
            temp_note=TemporaryNoteFactory.create_temp_content( real_instance=None, faculty=faculty, name=note_name, content_file=note_content)
            notification = Notification.objects.create(
                message=f"{request.user.first_name} {request.user.last_name} wants to add a note in {temp_note.faculty.course.department.name}/{temp_note.faculty.course.course_name}/{temp_note.faculty.name}",
                sender=request.user,
                type="add",
                content_type="note",
                content_id=temp_note.id
            )
            receivers = User.objects.filter(Q(role='master') | Q(department=dept_id) | Q(course=course_id))
            notification.recievers.add(*receivers)
            notification.save()
            subject.notify(request, "Request sent")
    return redirect('lec_notes', ins_id, dept_id, course_id, fac_id)


# Add Video
@login_required
def add_video(request,ins_id, dept_id, course_id, fac_id):
    faculty = get_object_or_404(Faculty, id=fac_id)
    if request.method == 'POST':
        video_name = request.POST.get('videoName')
        video_content = request.FILES.get('videoContent')
        if (request.user.institute==ins_id) or (request.user.department == dept_id) or (request.user.course == course_id):
            VideoFactory.create_content( faculty, video_name, video_content)
            proxy=QueryCacheProxy(request.user)
            proxy.delete_LecVideos_cache(ins_id, dept_id, course_id, fac_id)
            subject.notify(request, "Video has been added")
        else:
            temp_video=TemporaryVideoFactory.create_temp_content( real_instance=None, faculty=faculty, name=video_name, content_file=video_content)
            notification = Notification.objects.create(
                message=f"{request.user.first_name} {request.user.last_name} wants to add a video in {temp_video.faculty.course.department.name}/{temp_video.faculty.course.course_name}/{temp_video.faculty.name}",
                sender=request.user,
                type="add",
                content_type="video",
                content_id=temp_video.id
            )
            receivers = User.objects.filter(Q(role='master') | Q(department=dept_id) | Q(course=course_id))
            notification.recievers.add(*receivers)
            notification.save()
            subject.notify(request, "Request sent")
    return redirect('lec_videos', ins_id, dept_id, course_id, fac_id)
