from django.shortcuts import render
from lms. queryProxy import QueryCacheProxy

# Create your views here.
def commChat(request,ins_id):
    proxy = QueryCacheProxy(request.user)
    institute = proxy._get_institute(ins_id)  # Fetch departments via the proxy
    context={'institute':institute}
    return render(request, 'commChat.html',context)