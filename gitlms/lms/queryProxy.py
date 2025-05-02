from django.core.cache import cache
from .models import *
from django.contrib.auth.decorators import login_required

class QueryCacheProxy:
    def __init__(self, user):
        self.user = user
    @login_required
    def _get_institute(self, ins_id):
        key = f'institute_obj:{ins_id}'
        institute = cache.get(key)
        if institute:
            print(institute)
        if not institute:
            print("Institute not cached")
            institute = Institute.objects.get(id=ins_id)
            cache.set(key, institute, timeout=60 * 15)
        return institute
    @login_required
    def _get_department(self, ins_id,dept_id):
        institute=self._get_institute(ins_id)
        key = f'department_obj:{ ins_id}:{dept_id}'
        department = cache.get(key)
        if department:
            print(department)
        if not department:
            print("Department not cached")
            department = Department.objects.get(id=dept_id)
            cache.set(key, department, timeout=60 * 15)
        return department,institute
    @login_required
    def _get_course(self,  ins_id,dept_id, course_id):
        
        course_key = f'course_obj:{ ins_id}:{dept_id}:{course_id}'

        department, institute = self._get_department(ins_id,dept_id)
        
        course = cache.get(course_key)
        if course:
            print(course)
        if not course:
            print("Course not cached")
            course = Course.objects.get(id=course_id, department=department)
            cache.set(course_key, course, timeout=60 * 15)

        return course, department,institute
    @login_required
    def _get_faculty(self, ins_id, dept_id, course_id, fac_id):
        course, department,institute = self._get_course(ins_id,dept_id, course_id)
        faculty_key = f'faculty_obj:{ins_id}:{ ins_id}:{dept_id}:{course_id}:{fac_id}'

        faculty = cache.get(faculty_key)
        if faculty:
            print(faculty)
        if not faculty:
            print("Faculty not cached")
            faculty = Faculty.objects.get(id=fac_id, course=course)
            cache.set(faculty_key, faculty, timeout=60 * 15)

        return faculty, course, department,institute

    @login_required
    def get_institutes(self):
        key = 'all_institutes'
        institutes = cache.get(key)
        if institutes:
            print(institutes)
        if not institutes:
            print("institutes not cached yet")
            institutes = Institute.objects.all().order_by('name')
            cache.set(key, institutes, timeout=60 * 15)
        return institutes
    
    @login_required
    def get_departments(self,ins_id):
        institute=self._get_institute(ins_id)
        key = f'institute?{institute.id}'
        departments = cache.get(key)
        if departments:
            print(departments)
        if not departments:
            print("Departments not cached yet")
            departments = Department.objects.all().order_by('name')
            cache.set(key, departments, timeout=60 * 15)
        return departments,institute

    @login_required
    def get_deptCourses(self,ins_id, dept_id):
        department,institute = self._get_department(ins_id,dept_id)
        key = f'institute?{institute.id}/department?{department.id}'
        courses = cache.get(key)
        if courses:
            print(courses)
        if not courses:
            print("Courses not cached yet")
            courses = Course.objects.filter(department=department).order_by('course_name')
            cache.set(key, courses, timeout=60 * 15)
        return courses, department,institute

    @login_required
    def get_courseFacs(self,ins_id, dept_id, course_id):
        course, department,institute = self._get_course(ins_id,dept_id, course_id)
        key = f'institute?{institute.id}/department?{department.id}/course?{course.id}'
        faculties = cache.get(key)
        if faculties:
            print(faculties)
        if not faculties:
            print("Faculties not cached yet")
            faculties = Faculty.objects.filter(course=course).order_by('name')
            cache.set(key, faculties, timeout=60 * 15)
        return faculties,  course,department,institute

    @login_required
    def get_LecSlides(self,ins_id, dept_id, course_id, fac_id):
        faculty, course, department,institute = self._get_faculty(dept_id, course_id, fac_id)
        key = f'institute?{institute.id}/department?{department.id}/course?{course.id}/faculty?{faculty.id}/Lectures/Slides'
        slides = cache.get(key)
        if slides:
            print(slides)
        if not slides:
            print("Slides not cached yet")
            slides = Slide.objects.filter(faculty=faculty).order_by('-id')
            cache.set(key, slides, timeout=60 * 10)
        return slides, faculty, course, department,institute

    @login_required
    def get_LecVideos(self, dept_id, course_id, fac_id):
        faculty, course, department = self._get_faculty(dept_id, course_id, fac_id)
        key = f'institute?{institute.id}/department?{department.id}/course?{course.id}/faculty?{faculty.id}/Lectures/Videos'
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
        key = f'institute?{institute.id}/department?{department.id}/course?{course.id}/faculty?{faculty.id}/Lectures/Notes'
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
    def delete_institutes_cache(self):
        cache.delete('all_institutes')
        print("Deleted cache for: all_departments")

    @login_required
    def delete_departments_cache(self,ins_id):
        cache.delete(f'institute?{ins_id}')
        print(f"Deleted cache for: institute?{ins_id}")

    @login_required
    def delete_deptCourses_cache(self,ins_id, dept_id):
        cache.delete(f'institute?{ins_id}/department?{dept_id}')
        print(f"Deleted cache for: institute?{ins_id}/department?{dept_id}")

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
