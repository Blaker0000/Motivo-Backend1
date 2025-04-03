# motivo_backend/views.py

from django.http import HttpResponse

def homepage_view(request):
    return HttpResponse("<h1>Hello from Motivo!</h1>")
