from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("Welcome to Motivo Core!")

def my_first_template_view(request):
    # "hello.html" is the file we created in the templates folder
    return render(request, "hello.html")
