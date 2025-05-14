from lms.models import Department, Course,Institute
from django.http import JsonResponse
from django.core.cache import cache


def get_courses_by_department(request, department_id):
    department = Department.objects.get(id=department_id)
    courses = Course.objects.filter(department=department).values('id', 'course_code','course_name')
    return JsonResponse(list(courses), safe=False)

def get_institutes(request):
    institutes = Institute.objects.all().values('id', 'name')
    
    return JsonResponse(list(institutes), safe=False)

def get_departments_by_Institutes(request,ins_id):
    institute = Institute.objects.get(id=ins_id)
    departments = Department.objects.filter(institute=institute).values('id', 'name')
    
    return JsonResponse(list(departments), safe=False)



def get_department_and_course_ids(institute, cache_timeout=300):
    """
    Returns a tuple of (department_ids, course_ids) for the given institute.
    Caches the result for `cache_timeout` seconds.
    """
    cache_key = f"dept_course_ids_institute_{institute.id}"
    cached_data = cache.get(cache_key)
    if cached_data:
        return cached_data

    department_ids = list(
        Department.objects.filter(institute=institute).values_list('id', flat=True)
    )
    course_ids = list(
        Course.objects.filter(department__in=department_ids).values_list('id', flat=True)
    )

    result = (department_ids, course_ids)
    cache.set(cache_key, result, timeout=cache_timeout)
    return result
