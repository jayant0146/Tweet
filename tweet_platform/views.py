from django.shortcuts import HttpResponse
from django.shortcuts import render

def fn(request):
    return render(request, "index.html")