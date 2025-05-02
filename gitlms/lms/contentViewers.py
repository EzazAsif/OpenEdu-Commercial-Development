from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Slide,Video,Note

# To view a note
@login_required
def show_note(request,ins_id, dept_id, course_id, fac_id, note_id):
    note = Note.objects.get(id=note_id)
    context = {'note': note}
    return render(request, "contentViewers/noteViewer.html", context)


# To view a video
@login_required
def show_video(request,ins_id, dept_id, course_id, fac_id, video_id):
    video = Video.objects.get(id=video_id)
    context = {'video': video}
    return render(request, "contentViewers/videoViewer.html", context)



#To view the pdf
@login_required
def show_pdf(request,ins_id,dept_id, course_id,fac_id,slide_id):
    
    slide=Slide.objects.get(id=slide_id)
    context = {'slide':slide}
    
    return render(request,"contentViewers/pdfViewer.html",context)


