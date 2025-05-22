from django.shortcuts import render
from django.http import JsonResponse
from .qdrant_helper import search_qdrant

def semantic_search(request):
    query = request.GET.get("q", "")
    if not query:
        return JsonResponse({"error": "Query not provided"}, status=400)
    results = search_qdrant("lecture_materials", query)
    formatted = [
        {
            "title": r.payload.get("title"),
            "faculty": r.payload.get("faculty"),
            "uploaded_by": r.payload.get("uploaded_by"),
            "score": r.score
        }
        for r in results
    ]
    return JsonResponse({"results": formatted})


def ragPage(request):
    return render(request,'ragPage.html')