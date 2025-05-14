from django.http import JsonResponse
from accounts.models import User
from django.shortcuts import redirect
from django.http import JsonResponse
from elasticsearch_dsl import Q
from accounts.documents import UserDocument
from lms.queryProxy import QueryCacheProxy
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .queryfuncs import *





@csrf_exempt
def appoint_user(request):
    # Check if the request is a POST
    proxy=QueryCacheProxy(request.user)
    if request.method == 'POST':
        try:
            # Parse the incoming JSON data
            data = json.loads(request.body)
            user_id = data.get('user_id')
            appoint_role = data.get('appoint_role')  # The role being assigned (admin, moderator, user)
            department_id = data.get('department_id')  # Department ID for Admins
            course_id = data.get('course_id')  # Course ID for Moderators
            institute_id=data.get('institute_id')
            if (request.user.institute!= int(institute_id))and (request.user.department!= int(department_id)):
                return redirect('illegalactivity')
            
            # Retrieve the user object from the database
            user = User.objects.get(id=user_id)
            institute = proxy._get_institute(int(institute_id))
            department_ids,course_ids = get_department_and_course_ids(institute)
            if user.institute!=-1:
                return redirect('illegalactivity')
            if (user.department!=-1) and (not user.department in department_ids):
                return redirect('illegalactivity')
            if(user.course!=-1)and (not user.course in course_ids):
                return redirect('illegalactivity')
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





@login_required
def getUsers(request, string):
    q = Q(
        "bool",
        should=[
            Q("match", first_name={"query": string, "fuzziness": "AUTO"}),
            Q("match", last_name={"query": string, "fuzziness": "AUTO"}),
            Q("match", email={"query": string, "fuzziness": "AUTO"}),
        ],
        minimum_should_match=1
    )

    search_results = UserDocument.search().query(q)[:20]

    users = []
    seen_ids = set()
    for hit in search_results:
        if hit.meta.id in seen_ids:
            continue
        seen_ids.add(hit.meta.id)

        data = hit.to_dict()
        data["id"] = hit.meta.id
        users.append(data)

    return JsonResponse(users, safe=False)


@login_required
def getUsersappoint(request, string, ins_id):
    proxy=QueryCacheProxy(request.user)
    base_q = Q(
        "bool",
        should=[
            Q("match", first_name={"query": string, "fuzziness": "AUTO"}),
            Q("match", last_name={"query": string, "fuzziness": "AUTO"}),
            Q("match", email={"query": string, "fuzziness": "AUTO"}),
        ],
        minimum_should_match=1
    )

    # If user role is 'user', return all matching users without institute filtering
    if hasattr(request.user, 'role') and request.user.role == 'user':
        search_results = UserDocument.search().query(base_q)[:20]
    else:
        # ins_id is mandatory here; get institute, departments and courses
        institute = proxy._get_institute(ins_id)

        department_ids,course_ids = get_department_and_course_ids(institute)

        q_admins = Q('terms', department=list(department_ids))
        q_mods = Q('terms', course=list(course_ids))

        combined_q = Q(
            'bool',
            must=base_q,
            should=[q_admins, q_mods],
            minimum_should_match=1
        )

        search_results = UserDocument.search().query(combined_q)[:20]

    users = []
    seen_ids = set()
    for hit in search_results:
        if hit.meta.id in seen_ids:
            continue
        seen_ids.add(hit.meta.id)

        data = hit.to_dict()
        data["id"] = hit.meta.id
        users.append(data)
        if len(users) >= 20:
            break
    return JsonResponse(users, safe=False)
