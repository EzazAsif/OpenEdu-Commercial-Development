from django.http import JsonResponse
from lms.models import Department, Course,Institute
from accounts.models import User
from django.shortcuts import redirect
from django.http import JsonResponse
from elasticsearch_dsl import Q
from accounts.documents import UserDocument
from accounts.serializers import UserSerializer

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

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import json

@csrf_exempt
def appoint_user(request):
    # Check if the request is a POST
    
    if request.method == 'POST':
        try:
            # Parse the incoming JSON data
            data = json.loads(request.body)
            user_id = data.get('user_id')
            appoint_role = data.get('appoint_role')  # The role being assigned (admin, moderator, user)
            department_id = data.get('department_id')  # Department ID for Admins
            course_id = data.get('course_id')  # Course ID for Moderators
            institute_id=data.get('institute_id')
            print( request.user.institute," ",institute_id)
            if (request.user.institute!= int(institute_id))and (request.user.department!= int(department_id)):
                print("Illegal")
                return redirect('illegalactivity')
            # Retrieve the user object from the database
            user = User.objects.get(id=user_id)
            print(user_id,appoint_role,department_id ,course_id,institute_id)
            # Handle role assignment
            if appoint_role == 'admin':
                # Assign the user to a department for Admin role
                if department_id:
                    user.role = 'admin'
                    user.department = department_id
                    user.course = -1  # Remove course if admin is assigned
                else:
                    return JsonResponse({"status": "error", "message": "Department ID is required for Admin."})
            
            elif appoint_role == 'moderator':
                # Assign the user to a course for Moderator role
                if course_id:
                    user.role = 'mod'
                    user.course = course_id
                    user.department = -1  # Remove department if moderator is assigned
                else:
                    return JsonResponse({"status": "error", "message": "Course ID is required for Moderator."})
            
            elif appoint_role == 'user':

                # For User role, reset department and course
                user.role = 'user'
                user.department = -1
                user.course = -1
            
            else:
                return JsonResponse({"status": "error", "message": "Invalid role specified."})

            # Save the user with the new role assignment
           
            user.save()

            return JsonResponse({"status": "success", "message": f"Role {appoint_role} assigned successfully!"})

        except Exception as e:
            return JsonResponse({"status": "error", "message": f"Error: {str(e)}"})
    
    # If the request is not a POST
    return JsonResponse({"status": "error", "message": "Invalid request method."})





def getUsers(request, string):
    q = Q(
        "bool",
        should=[
            Q("match_phrase_prefix", first_name=string),
            Q("match_phrase_prefix", last_name=string),
            Q("match_phrase_prefix", email=string),
        ],
        minimum_should_match=1
    )
    search_results = UserDocument.search().query(q)[:20]
    user_ids = [hit.meta.id for hit in search_results]
    users = User.objects.filter(id__in=user_ids)
    serialized = UserSerializer(users, many=True)
    return JsonResponse(serialized.data, safe=False)
