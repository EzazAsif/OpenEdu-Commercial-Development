from django.urls import path
from .views import *
from .add_funcs import *
from .update_funcs import *
from .delete_funcs import *


urlpatterns = []

navigatelms=[
    path('', institutes, name='institutes'),
    path('institutes', institutes, name='institutes'),
    path('institute=<int:ins_id>', departments, name='departments'),
    path('institute=<int:ins_id>/department=<int:id>/', deptcourses, name='deptcourses'),
    path('institute=<int:ins_id>/department=<int:dept_id>/course=<int:course_id>', course_facs, name='course_facs'),
    path('institute=<int:ins_id>/department=<int:dept_id>/course=<int:course_id>/faculty=<int:fac_id>',fac_lecs, name='fac_lecs'),
    path('institute=<int:ins_id>/department=<int:dept_id>/course=<int:course_id>/faculty=<int:fac_id>/Lectures/slides',lec_slides, name='lec_slides'),
    path('institute=<int:ins_id>/department=<int:dept_id>/course=<int:course_id>/faculty=<int:fac_id>/Lectures/videos', lec_videos, name='lec_videos'),
    path('institute=<int:ins_id>/department=<int:dept_id>/course=<int:course_id>/faculty=<int:fac_id>/Lectures/notes', lec_notes, name='lec_notes'),
]

showcontents=[
path('institute=<int:ins_id>/department=<int:dept_id>/course=<int:course_id>/faculty=<int:fac_id>/Lectures/slides/slide=<int:slide_id>',show_pdf, name='show_pdf'),
path('institute=<int:ins_id>/department=<int:dept_id>/course=<int:course_id>/faculty=<int:fac_id>/Lectures/videos/video=<int:video_id>', show_video, name='show_video'),
path('institute=<int:ins_id>/department=<int:dept_id>/course=<int:course_id>/faculty=<int:fac_id>/Lectures/notes/note=<int:note_id>', show_note, name='show_note')
]

addUrl = [
    path('institute=<int:ins_id>/add', add_dept, name='add_dept'),
    path('institute=<int:ins_id>/department=<int:dept_id>/add', add_course, name='add_course'),
    path('institute=<int:ins_id>/department=<int:dept_id>/course=<int:course_id>/add', add_fac, name='add_fac'),
    path('institute=<int:ins_id>/department=<int:dept_id>/course=<int:course_id>/faculty=<int:fac_id>/Lectures/slides/add', add_slide, name='add_slide'),
    path('institute=<int:ins_id>/department=<int:dept_id>/course=<int:course_id>/faculty=<int:fac_id>/Lectures/videos/add', add_video, name='add_video'),
    path('institute=<int:ins_id>/department=<int:dept_id>/course=<int:course_id>/faculty=<int:fac_id>/Lectures/notes/add', add_note, name='add_note'),
]

updateUrl = [
    path('institute=<int:ins_id>/update/<int:dept_id>', update_dept, name='update_dept'),
    path('institute=<int:ins_id>/department=<int:dept_id>/update/<int:course_id>', update_course, name='update_course'),
    path('institute=<int:ins_id>/department=<int:dept_id>/course=<int:course_id>/update/<int:fac_id>', update_fac, name='update_fac'),
    path('institute=<int:ins_id>/department=<int:dept_id>/course=<int:course_id>/faculty=<int:fac_id>/Lectures/slides/update/<int:slide_id>', update_slide, name='update_slide'),
    path('institute=<int:ins_id>/department=<int:dept_id>/course=<int:course_id>/faculty=<int:fac_id>/Lectures/videos/update/<int:video_id>', update_video, name='update_video'),
    path('institute=<int:ins_id>/department=<int:dept_id>/course=<int:course_id>/faculty=<int:fac_id>/Lectures/notes/update/<int:note_id>', update_note, name='update_note'),
]

deleteUrl = [
    path('institute=<int:ins_id>/delete/<int:dept_id>', delete_dept, name='delete_dept'),
    path('institute=<int:ins_id>/department=<int:dept_id>/delete/<int:course_id>', delete_course, name='delete_course'),
    path('institute=<int:ins_id>/department=<int:dept_id>/course=<int:course_id>/delete/<int:fac_id>', delete_fac, name='delete_fac'),
    path('institute=<int:ins_id>/department=<int:dept_id>/course=<int:course_id>/faculty=<int:fac_id>/Lectures/slides/delete/<int:slide_id>', delete_slide, name='delete_slide'),
    path('institute=<int:ins_id>/department=<int:dept_id>/course=<int:course_id>/faculty=<int:fac_id>/Lectures/videos/delete/<int:video_id>', delete_video, name='delete_video'),
    path('institute=<int:ins_id>/department=<int:dept_id>/course=<int:course_id>/faculty=<int:fac_id>/Lectures/notes/delete/<int:note_id>', delete_note, name='delete_note'),
]


urlpatterns+=navigatelms
urlpatterns+=showcontents
urlpatterns+=addUrl
urlpatterns+=updateUrl
urlpatterns+=deleteUrl