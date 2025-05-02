from django.core.cache import cache
from .models import *
from django.contrib.auth.decorators import login_required

class QueryCacheProxy:
    def __init__(self, user):
        self.user = user
    def _get_institute(self, ins_id):
        key = f'institute_obj:{ins_id}'
        Institute = cache.get(key)
        if Institute:
            print(Institute)
        if not Institute:
            print("Institute not cached")
            Institute = Institute.objects.get(id=ins_id)
            cache.set(key, Institute, timeout=60 * 15)
        return Institute

    def _get_department(self, dept_id):
        key = f'department_obj:{dept_id}'
        department = cache.get(key)
        if department:
            print(department)
        if not department:
            print("Department not cached")
            department = Department.objects.get(id=dept_id)
            cache.set(key, department, timeout=60 * 15)
        return department

    def _get_course(self, dept_id, course_id):
        
        course_key = f'course_obj:{dept_id}:{course_id}'

        department = self._get_department(dept_id)
        
        course = cache.get(course_key)
        if course:
            print(course)
        if not course:
            print("Course not cached")
            course = Course.objects.get(id=course_id, department=department)
            cache.set(course_key, course, timeout=60 * 15)

        return course, department

    def _get_faculty(self, dept_id, course_id, fac_id):
        course, department = self._get_course(dept_id, course_id)
        faculty_key = f'faculty_obj:{dept_id}:{course_id}:{fac_id}'

        faculty = cache.get(faculty_key)
        if faculty:
            print(faculty)
        if not faculty:
            print("Faculty not cached")
            faculty = Faculty.objects.get(id=fac_id, course=course)
            cache.set(faculty_key, faculty, timeout=60 * 15)

        return faculty, course, department


    @login_required
    def get_departments(self):
        key = 'all_departments'
        departments = cache.get(key)
        if departments:
            print(departments)
        if not departments:
            print("Departments not cached yet")
            departments = Department.objects.all().order_by('name')
            cache.set(key, departments, timeout=60 * 15)
        return departments

    @login_required
    def get_deptCourses(self, dept_id):
        department = self._get_department(dept_id)
        key = f'department?{department.id}'
        courses = cache.get(key)
        if courses:
            print(courses)
        if not courses:
            print("Courses not cached yet")
            courses = Course.objects.filter(department=department).order_by('course_name')
            cache.set(key, courses, timeout=60 * 15)
        return courses, department

    @login_required
    def get_courseFacs(self, dept_id, course_id):
        course, department = self._get_course(dept_id, course_id)
        key = f'department?{department.id}/course?{course.id}'
        faculties = cache.get(key)
        if faculties:
            print(faculties)
        if not faculties:
            print("Faculties not cached yet")
            faculties = Faculty.objects.filter(course=course).order_by('name')
            cache.set(key, faculties, timeout=60 * 15)
        return faculties, department, course

    @login_required
    def get_LecSlides(self, dept_id, course_id, fac_id):
        faculty, course, department = self._get_faculty(dept_id, course_id, fac_id)
        key = f'department?{department.id}/course?{course.id}/faculty?{faculty.id}/Lectures/Slides'
        slides = cache.get(key)
        if slides:
            print(slides)
        if not slides:
            print("Slides not cached yet")
            slides = Slide.objects.filter(faculty=faculty).order_by('-id')
            cache.set(key, slides, timeout=60 * 10)
        return slides, department, course, faculty

    @login_required
    def get_LecVideos(self, dept_id, course_id, fac_id):
        faculty, course, department = self._get_faculty(dept_id, course_id, fac_id)
        key = f'department?{department.id}/course?{course.id}/faculty?{faculty.id}/Lectures/Videos'
        videos = cache.get(key)
        if videos:
            print(videos)
        if not videos:
            print("Videos not cached yet")
            videos = Video.objects.filter(faculty=faculty).order_by('-id')
            cache.set(key, videos, timeout=60 * 10)
        return videos, department, course, faculty

    @login_required
    def get_LecNotes(self, dept_id, course_id, fac_id):
        faculty, course, department = self._get_faculty(dept_id, course_id, fac_id)
        key = f'department?{department.id}/course?{course.id}/faculty?{faculty.id}/Lectures/Notes'
        notes = cache.get(key)
        if notes:
            print(notes)
        if not notes:
            print("Notes not cached yet")
            notes = Note.objects.filter(faculty=faculty).order_by('-id')
            cache.set(key, notes, timeout=60 * 10)
        return notes, department, course, faculty

    # Cache deletion methods
    @login_required
    def delete_departments_cache(self):
        cache.delete('all_departments')
        print("Deleted cache for: all_departments")

    @login_required
    def delete_deptCourses_cache(self, dept_id):
        cache.delete(f'department?{dept_id}')
        print(f"Deleted cache for: department?{dept_id}")

    @login_required
    def delete_courseFacs_cache(self, dept_id, course_id):
        cache.delete(f'department?{dept_id}/course?{course_id}')
        print(f"Deleted cache for: department?{dept_id}/course?{course_id}")

    @login_required
    def delete_LecSlides_cache(self, dept_id, course_id, fac_id):
        cache.delete(f'department?{dept_id}/course?{course_id}/faculty?{fac_id}/Lectures/Slides')
        print(f"Deleted cache for: department?{dept_id}/course?{course_id}/faculty?{fac_id}/Lectures/Slides")

    @login_required
    def delete_LecVideos_cache(self, dept_id, course_id, fac_id):
        cache.delete(f'department?{dept_id}/course?{course_id}/faculty?{fac_id}/Lectures/Videos')
        print(f"Deleted cache for: department?{dept_id}/course?{course_id}/faculty?{fac_id}/Lectures/Videos")

    @login_required
    def delete_LecNotes_cache(self, dept_id, course_id, fac_id):
        cache.delete(f'department?{dept_id}/course?{course_id}/faculty?{fac_id}/Lectures/Notes')
        print(f"Deleted cache for: department?{dept_id}/course?{course_id}/faculty?{fac_id}/Lectures/Notes")
