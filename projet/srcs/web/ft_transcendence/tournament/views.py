from django.shortcuts import render
from django.http import HttpResponse

def some_view(request):
    return HttpResponse("Hello, this is some view!")