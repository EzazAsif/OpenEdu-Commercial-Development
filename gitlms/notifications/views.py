from django.shortcuts import render,redirect, get_object_or_404
from .models import Notification
from lms.models import *
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from lms.queryProxy import QueryCacheProxy
from myRag.qdrant_helper import push_to_qdrant

# Create your views here.
@login_required
def notifications(request):
    notifications = Notification.objects.filter(recievers=request.user).order_by('-created_at')

    context={'notifications':notifications}
    return render(request,"notifications.html",context)



@login_required
def reject_not(request, not_id):
    notification = get_object_or_404(Notification, id=not_id)
    if request.user not in notification.recievers.all():
         return redirect('illegalactivity')
    # Ensure the notification type is 'add' or 'update'
    print(f"Notification type: {notification.type}, Content type: {notification.content_type}")
    if notification.type in ['add', 'update']:
        # Determine the content model based on the notification content_type
        if notification.content_type == 'slide':
            content_model = Slide
            temp_content_model = temp_Slide
        elif notification.content_type == 'video':
            content_model = Video
            temp_content_model = temp_Video
        elif notification.content_type == 'note':
            content_model = Note
            temp_content_model = temp_Note
        else:
            # Invalid content_type, handle the error with a clear message
            print(f"Invalid content type '{notification.content_type}' provided.")
            raise ValueError(f"Invalid content type '{notification.content_type}' provided.")

        # Try to fetch the temporary content from the appropriate model and delete it
        try:
            print(f"Attempting to fetch temporary content with id {notification.content_id} of type {notification.content_type}")
            temp_content = temp_content_model.objects.get(id=notification.content_id)
            print(f"Temporary content found: {temp_content}")
            temp_content.delete()  # Delete the temporary content instance
            print(f"Temporary content with id {notification.content_id} deleted")

        except temp_content_model.DoesNotExist:
            # If temporary content doesn't exist, log the message and redirect to notifications page
            print(f"Temporary content with id {notification.content_id} does not exist.")
            return redirect("notifications")

    # Create a rejection notification for the user who requested it
    print(f"Creating rejection notification for user {notification.sender}")
    Not = Notification.objects.create(
            sender=request.user,
            
            message=f"Your {notification.type} request for {notification.content_type} has been Rejected by {request.user.first_name} {request.user.last_name} ({request.user.role})",
            type='inf'
        )

        # Fix: Add the receiver properly
    reciever = [notification.sender]
    Not.recievers.add(*reciever)  # Use *reciever to unpack the list and add to the ManyToMany field
    Not.save()
    print(f"Rejection notification created and sent to {notification.sender}")

    # Delete the original notification after rejection
    print(f"Deleting the original notification with id {not_id}")
    notification.delete()

    # Redirect back to the notifications page
    print("Redirecting to notifications page")
    return redirect("notifications")


@login_required
def approve_not(request, not_id):
    
    notification = get_object_or_404(Notification, id=not_id)
    if request.user not in notification.recievers.all():
         return redirect('illegalactivity')
    proxy=QueryCacheProxy(request.user)
    # Ensure the notification type is 'add', 'update', or 'delete'
    if notification.type in ['add', 'update', 'delete']:
        # Manually map the content_type to corresponding models
        content_map = {
            'slide': (Slide, temp_Slide,proxy.delete_LecSlides_cache),
            'video': (Video, temp_Video,proxy.delete_LecVideos_cache),
            'note': (Note, temp_Note,proxy.delete_LecNotes_cache)
        }

        # Check if the content_type is valid and retrieve the models
        if notification.content_type in content_map:
            content_model, temp_content_model,contenDeleteProxy = content_map[notification.content_type]
        else:
            raise ValueError(f"Invalid content type '{notification.content_type}' provided.")  # Handle invalid type

        # Handle 'add' logic (no need to query for the object, just create it)
        if notification.type == 'add':
            temp_content = get_object_or_404(temp_content_model, id=notification.content_id)

            # Create the real content instance directly from the temporary content
            real_content = content_model.objects.create(
                name=temp_content.name,
                faculty=temp_content.faculty,
                content=temp_content.content,  # Using content from the temporary content
                uploaded_by=temp_content.uploaded_by
            )
            push_to_qdrant( real_content.content, real_content.name,real_content.content.url , "slide")
            # Set the real_content_id in the notification
            notification.real_content_id = real_content.id
            notification.save()
            
            # Delete the temporary content instance after approval
            temp_content.delete()
            contenDeleteProxy(real_content.faculty.course.department.institute.id,real_content.faculty.course.department.id,real_content.faculty.course.id,real_content.faculty.id)
            


        # Handle 'update' logic
        elif notification.type == 'update':
            content = get_object_or_404(content_model, id=notification.real_content_id)

            # Update the content fields using the name and content from the temporary content
            temp_content = get_object_or_404(temp_content_model, id=notification.content_id)  # Get associated temp content
            if temp_content.name:
                content.name = temp_content.name  # Update the real content's name
            if temp_content.content:
                content.content = temp_content.content  # Update the real content's content
            if temp_content.uploaded_by:
                content.uploaded_by = temp_content.uploaded_by
            content.save()  # Save the updated real content to the database
            if temp_content.content:
                push_to_qdrant( content.content, content.name,content.content.url , "slide")
            # Set the real_content_id to the updated content ID
            notification.real_content_id = content.id
            notification.save()

            # Delete the temporary content after updating
            temp_content.delete()
            contenDeleteProxy(content.faculty.course.department.id,content.faculty.course.id,content.faculty.id)

        # Handle 'delete' logic
        elif notification.type == 'delete':
            try:
                content = content_model.objects.get(id=notification.real_content_id)
                contenDeleteProxy(content.faculty.course.department.id,content.faculty.course.id,content.faculty.id)
                # Delete the real content instance
                content.delete()
   
                # Set the real_content_id to null (since it's deleted)
                Notification.objects.filter(Q(real_content_id=notification.real_content_id) & Q(content_type=notification.content_type)).delete()
                
            
            except content_model.DoesNotExist:
                # Handle case if the content to be deleted does not exist
                
                return redirect("notifications")
            
        # Create an approval notification for the user who requested it
        Not = Notification.objects.create(
            sender=request.user,
            
            message=f"Your {notification.type} request for {notification.content_type} has been approved by {request.user.first_name} {request.user.last_name} ({request.user.role})",
            type='inf'
        )

        # Fix: Add the receiver properly
        reciever = [notification.sender]
        Not.recievers.add(*reciever)  # Use *reciever to unpack the list and add to the ManyToMany field

    
    
    notification.delete()
    
    # Redirect back to the notifications page
    return redirect("notifications")

@login_required
def view_not(request,not_id):
    notification = get_object_or_404(Notification, id=not_id)
    if request.user not in notification.recievers.all():
         return redirect('illegalactivity')
    content_map={'video':Video,'slide':Slide,'note':Note}
    temp_content_map={'video':temp_Video,'slide':temp_Slide,'note':temp_Note}
    content=content_map[notification.content_type]
    temp_content=temp_content_map[notification.content_type]
    real_content=None
    update_content=None
    if notification.type == "update":
        real_content=content.objects.get(id=notification.real_content_id)
        update_content=temp_content.objects.get(id=notification.content_id)
    elif(notification.type == "delete"):
        real_content=content.objects.get(id=notification.real_content_id)
    elif(notification.type == "add"):
        update_content=temp_content.objects.get(id=notification.content_id)
    context={'real_content':real_content,'update_content':update_content,'notification':notification}
    print("context",context)
    if notification.content_type =="video":
        return render(request,'viewNotificationDetailsVideo.html',context)
    return render(request,"viewNotificationDetailsSlide.html",context)


@login_required
def notifications2(request):
   
    return render(request,"notification-2.html")
